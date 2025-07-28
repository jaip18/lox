from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, func
from models import NBAPlayer, NBAPlayerGamelogs, NBAPlayerProps, NBAEvent
from database import SessionLocal
import crud
import apis.nba_api_utils as nba_api
import apis.odds_api as odds_api
from typing import List, Dict, Optional, Tuple
import statistics
import pandas as pd
from datetime import datetime, timedelta
from dataclasses import dataclass
import time


@dataclass
class PlayerConsistency:
    player_id: int
    player_name: str
    stat_type: str
    mean: float
    std_dev: float
    consistency_score: float
    games_analyzed: int
    hit_rate_over: float
    hit_rate_under: float
    recent_form: List[float]


class NBABettingAlgorithm:
    def __init__(self, db_session: Session = None):
        self.db = db_session or SessionLocal()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db:
            self.db.close()

    def get_player_gamelog_stats(self, player_id: int, stat_column: str, days_back: int = 30) -> List[float]:
        """
        Fetch player statistics for a specific stat over the last N days
        """
        cutoff_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        # Map stat names to database columns
        stat_mapping = {
            'points': 'points',
            'rebounds': 'rebounds', 
            'assists': 'assists',
            'steals': 'steals',
            'blocks': 'blocks',
            'turnovers': 'turnovers',
            'three_pt_made': 'three_pt_made',
            'field_goals_made': 'field_goals_made',
            'free_throw_made': 'free_throw_made'
        }
        
        if stat_column not in stat_mapping:
            raise ValueError(f"Invalid stat column: {stat_column}")
        
        db_column = getattr(NBAPlayerGamelogs, stat_mapping[stat_column])
        
        gamelogs = self.db.query(NBAPlayerGamelogs).join(NBAPlayer).filter(
            and_(
                NBAPlayer.player_id == player_id,
                NBAPlayerGamelogs.game_date >= cutoff_date,
                db_column.isnot(None)
            )
        ).order_by(desc(NBAPlayerGamelogs.game_date)).all()
        
        return [getattr(log, stat_mapping[stat_column]) for log in gamelogs if getattr(log, stat_mapping[stat_column]) is not None]

    def calculate_consistency_metrics(self, values: List[float]) -> Dict:
        """
        Calculate standard deviation and consistency metrics for a list of values
        """
        if len(values) < 3:
            return {
                'mean': 0,
                'std_dev': float('inf'),
                'consistency_score': 0,
                'coefficient_of_variation': float('inf')
            }
        
        mean_val = statistics.mean(values)
        std_dev = statistics.stdev(values)
        
        # Consistency score: lower std dev relative to mean = higher consistency
        coefficient_of_variation = std_dev / mean_val if mean_val > 0 else float('inf')
        consistency_score = 1 / (1 + coefficient_of_variation) if coefficient_of_variation != float('inf') else 0
        
        return {
            'mean': mean_val,
            'std_dev': std_dev,
            'consistency_score': consistency_score,
            'coefficient_of_variation': coefficient_of_variation
        }

    def calculate_prop_hit_rates(self, values: List[float], prop_line: float) -> Tuple[float, float]:
        """
        Calculate hit rates for over/under a specific prop line
        """
        if not values:
            return 0.0, 0.0
        
        over_hits = sum(1 for val in values if val > prop_line)
        under_hits = sum(1 for val in values if val < prop_line)
        total_games = len(values)
        
        over_rate = over_hits / total_games
        under_rate = under_hits / total_games
        
        return over_rate, under_rate

    def analyze_player_consistency(self, 
                                 player_id: int, 
                                 stat_type: str, 
                                 days_back: int = 30, 
                                 prop_line: float = None) -> PlayerConsistency:
        """
        Analyze a single player's consistency for a specific stat
        """
        # Get player info
        player = self.db.query(NBAPlayer).filter(NBAPlayer.player_id == player_id).first()
        if not player:
            raise ValueError(f"Player with ID {player_id} not found")
        
        # Get stat values
        stat_values = self.get_player_gamelog_stats(player_id, stat_type, days_back)
        
        if not stat_values:
            return PlayerConsistency(
                player_id=player_id,
                player_name=player.name,
                stat_type=stat_type,
                mean=0,
                std_dev=float('inf'),
                consistency_score=0,
                games_analyzed=0,
                hit_rate_over=0,
                hit_rate_under=0,
                recent_form=[]
            )
        
        # Calculate consistency metrics
        metrics = self.calculate_consistency_metrics(stat_values)
        
        # Calculate hit rates if prop line provided
        hit_rate_over, hit_rate_under = 0.0, 0.0
        if prop_line is not None:
            hit_rate_over, hit_rate_under = self.calculate_prop_hit_rates(stat_values, prop_line)
        
        return PlayerConsistency(
            player_id=player_id,
            player_name=player.name,
            stat_type=stat_type,
            mean=metrics['mean'],
            std_dev=metrics['std_dev'],
            consistency_score=metrics['consistency_score'],
            games_analyzed=len(stat_values),
            hit_rate_over=hit_rate_over,
            hit_rate_under=hit_rate_under,
            recent_form=stat_values[:5]  # Last 5 games
        )

    def find_most_consistent_players(self, 
                                   stat_type: str, 
                                   prop_line: float = None,
                                   days_back: int = 30, 
                                   min_games: int = 5,
                                   team_filter: str = None,
                                   top_n: int = 20) -> List[PlayerConsistency]:
        """
        Find the most consistent players for a specific stat type
        """
        # Get active players
        query = self.db.query(NBAPlayer).filter(NBAPlayer.team_name.isnot(None))
        
        if team_filter:
            query = query.filter(NBAPlayer.team_name == team_filter)
        
        players = query.all()
        
        consistencies = []
        
        for player in players:
            try:
                consistency = self.analyze_player_consistency(
                    player.player_id, 
                    stat_type, 
                    days_back, 
                    prop_line
                )
                
                # Filter by minimum games
                if consistency.games_analyzed >= min_games:
                    consistencies.append(consistency)
                    
            except Exception as e:
                print(f"Error analyzing player {player.name}: {e}")
                continue
        
        # Sort by consistency score (higher is better)
        consistencies.sort(key=lambda x: x.consistency_score, reverse=True)
        
        return consistencies[:top_n]

    def analyze_prop_value(self, 
                          player_id: int, 
                          stat_type: str, 
                          prop_line: float,
                          days_back: int = 30) -> Dict:
        """
        Analyze the value of a specific prop bet based on historical performance
        """
        consistency = self.analyze_player_consistency(player_id, stat_type, days_back, prop_line)
        
        # Get current prop odds if available
        current_props = self.db.query(NBAPlayerProps).join(NBAPlayer).filter(
            and_(
                NBAPlayer.player_id == player_id,
                NBAPlayerProps.prop_type.contains(stat_type.lower())
            )
        ).order_by(desc(NBAPlayerProps.last_update)).first()
        
        # Calculate expected value based on hit rates
        over_probability = consistency.hit_rate_over
        under_probability = consistency.hit_rate_under
        
        analysis = {
            'player_name': consistency.player_name,
            'stat_type': stat_type,
            'prop_line': prop_line,
            'historical_mean': consistency.mean,
            'std_deviation': consistency.std_dev,
            'consistency_score': consistency.consistency_score,
            'over_hit_rate': over_probability,
            'under_hit_rate': under_probability,
            'games_analyzed': consistency.games_analyzed,
            'recent_form': consistency.recent_form,
            'recommendation': self._generate_recommendation(consistency, prop_line)
        }
        
        if current_props:
            analysis['current_over_odds'] = current_props.over_odds
            analysis['current_under_odds'] = current_props.under_odds
            analysis['bookmaker'] = current_props.bookmaker
        
        return analysis

    def _generate_recommendation(self, consistency: PlayerConsistency, prop_line: float) -> str:
        """
        Generate a betting recommendation based on consistency analysis
        """
        if consistency.games_analyzed < 5:
            return "INSUFFICIENT_DATA"
        
        mean_diff = consistency.mean - prop_line
        hit_rate_threshold = 0.6  # 60% hit rate threshold
        consistency_threshold = 0.7  # Consistency score threshold
        
        if consistency.consistency_score >= consistency_threshold:
            if consistency.hit_rate_over >= hit_rate_threshold and mean_diff > consistency.std_dev * 0.5:
                return "STRONG_OVER"
            elif consistency.hit_rate_under >= hit_rate_threshold and mean_diff < -consistency.std_dev * 0.5:
                return "STRONG_UNDER"
            elif consistency.hit_rate_over >= 0.55:
                return "LEAN_OVER"
            elif consistency.hit_rate_under >= 0.55:
                return "LEAN_UNDER"
        
        return "NO_PLAY"

    def populate_player_gamelogs(self, player_id: int, max_games: int = 50) -> bool:
        """
        Populate gamelogs for a specific player using NBA API
        """
        try:
            print(f"🔄 Fetching gamelogs for player ID: {player_id}")
            
            # Check if player exists in our database
            player = self.db.query(NBAPlayer).filter(NBAPlayer.player_id == player_id).first()
            if not player:
                print(f"❌ Player {player_id} not found in database")
                return False
            
            # Fetch gamelogs from NBA API
            gamelogs = nba_api.fetch_player_game_logs(player_id)
            
            if not gamelogs:
                print(f"⚠️ No gamelogs found for player {player.name}")
                return False
            
            # Process and store gamelogs (limit to max_games)
            stored_count = 0
            for gamelog in gamelogs[:max_games]:
                try:
                    existing_log = crud.get_NBAplayer_gamelog(
                        self.db, 
                        str(player_id), 
                        str(gamelog.get('Game_ID', ''))
                    )
                    
                    if not existing_log:
                        crud.create_player_gamelog(self.db, gamelog)
                        stored_count += 1
                        
                except Exception as e:
                    print(f"⚠️ Error storing gamelog for {player.name}: {e}")
                    continue
            
            print(f"✅ Stored {stored_count} new gamelogs for {player.name}")
            return True
            
        except Exception as e:
            print(f"❌ Error populating gamelogs for player {player_id}: {e}")
            return False

    def bulk_populate_gamelogs(self, team_name: str = None, max_players: int = 10, delay: int = 3) -> Dict:
        """
        Populate gamelogs for multiple players (by team or all active players)
        """
        results = {
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'players_processed': []
        }
        
        try:
            # Get players to process
            query = self.db.query(NBAPlayer).filter(NBAPlayer.team_name.isnot(None))
            
            if team_name:
                query = query.filter(NBAPlayer.team_name == team_name)
            
            players = query.limit(max_players).all()
            
            for player in players:
                try:
                    # Check if we already have recent gamelogs
                    recent_logs = self.db.query(NBAPlayerGamelogs).filter(
                        NBAPlayerGamelogs.player_id == player.id
                    ).limit(5).all()
                    
                    if len(recent_logs) >= 5:
                        results['skipped'] += 1
                        results['players_processed'].append({
                            'name': player.name,
                            'status': 'skipped',
                            'reason': 'sufficient_data'
                        })
                        continue
                    
                    # Add delay to avoid rate limiting
                    time.sleep(delay)
                    
                    success = self.populate_player_gamelogs(player.player_id)
                    
                    if success:
                        results['successful'] += 1
                        results['players_processed'].append({
                            'name': player.name,
                            'status': 'success'
                        })
                    else:
                        results['failed'] += 1
                        results['players_processed'].append({
                            'name': player.name,
                            'status': 'failed'
                        })
                        
                except Exception as e:
                    results['failed'] += 1
                    results['players_processed'].append({
                        'name': player.name,
                        'status': 'error',
                        'error': str(e)
                    })
                    continue
            
            return results
            
        except Exception as e:
            print(f"❌ Error in bulk gamelog population: {e}")
            return results

    def sync_current_props_with_odds_api(self, league_id: str = "NBA") -> Dict:
        """
        Sync current player props with your odds API
        """
        results = {
            'events_processed': 0,
            'props_updated': 0,
            'errors': []
        }
        
        try:
            # Fetch current NBA events
            today_iso = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
            events = odds_api.fetch_current_events_by_league(league_id, today_iso)
            
            for event_data in events:
                try:
                    # Get or create event in database
                    existing_event = crud.get_NBAevent_by_id(self.db, event_data["eventID"])
                    
                    if not existing_event:
                        # Create league if needed
                        league_data = odds_api.fetch_league_by_ID(league_id)
                        if league_data:
                            league = crud.create_league(self.db, league_data)
                            existing_event = crud.create_NBAevent(self.db, event_data, league.id)
                    
                    if existing_event:
                        # Fetch odds/props for this event
                        odds_data = odds_api.fetch_odds_by_event(event_data["eventID"])
                        
                        # Process player props if available
                        # Note: This depends on your odds API structure for player props
                        # You may need to modify based on actual API response format
                        
                        results['events_processed'] += 1
                        
                except Exception as e:
                    results['errors'].append({
                        'event_id': event_data.get("eventID", "unknown"),
                        'error': str(e)
                    })
                    continue
            
            return results
            
        except Exception as e:
            results['errors'].append({'general_error': str(e)})
            return results
        """
        Get team-level consistency rankings for a specific stat
        """
        teams = self.db.query(NBAPlayer.team_name).distinct().all()
        team_rankings = {}
        
        for team_tuple in teams:
            team_name = team_tuple[0]
            if not team_name:
                continue
            
            team_players = self.find_most_consistent_players(
                stat_type=stat_type,
                days_back=days_back,
                team_filter=team_name,
                top_n=15
            )
            
            if team_players:
                avg_consistency = statistics.mean([p.consistency_score for p in team_players])
                team_rankings[team_name] = {
                    'average_consistency': avg_consistency,
                    'top_players': team_players[:5],
                    'total_players_analyzed': len(team_players)
                }
        
    def get_team_consistency_rankings(self, stat_type: str, days_back: int = 30) -> Dict:
        """
        Get team-level consistency rankings for a specific stat
        """
        teams = self.db.query(NBAPlayer.team_name).distinct().all()
        team_rankings = {}
        
        for team_tuple in teams:
            team_name = team_tuple[0]
            if not team_name:
                continue
            
            team_players = self.find_most_consistent_players(
                stat_type=stat_type,
                days_back=days_back,
                team_filter=team_name,
                top_n=15
            )
            
            if team_players:
                avg_consistency = statistics.mean([p.consistency_score for p in team_players])
                team_rankings[team_name] = {
                    'average_consistency': avg_consistency,
                    'top_players': team_players[:5],
                    'total_players_analyzed': len(team_players)
                }
        
        return dict(sorted(team_rankings.items(), key=lambda x: x[1]['average_consistency'], reverse=True))

    def get_daily_prop_recommendations(self, 
                                     stat_types: List[str] = None, 
                                     min_consistency_score: float = 0.7,
                                     min_hit_rate: float = 0.6,
                                     days_back: int = 20) -> Dict:
        """
        Get daily prop recommendations across multiple stat types
        """
        if stat_types is None:
            stat_types = ['points', 'rebounds', 'assists', 'three_pt_made']
        
        recommendations = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'criteria': {
                'min_consistency_score': min_consistency_score,
                'min_hit_rate': min_hit_rate,
                'days_analyzed': days_back
            },
            'recommendations': []
        }
        
        # Get today's events
        today = datetime.now().strftime('%Y-%m-%d')
        today_events = self.db.query(NBAEvent).filter(
            func.date(NBAEvent.start_time) == today
        ).all()
        
        # Get players playing today
        playing_today = []
        for event in today_events:
            # Get players from both teams
            home_players = self.db.query(NBAPlayer).filter(
                NBAPlayer.team_name == event.home_team
            ).all()
            away_players = self.db.query(NBAPlayer).filter(
                NBAPlayer.team_name == event.away_team
            ).all()
            
            playing_today.extend(home_players + away_players)
        
        # Analyze each player for each stat type
        for player in playing_today:
            for stat_type in stat_types:
                try:
                    consistency = self.analyze_player_consistency(
                        player.player_id, 
                        stat_type, 
                        days_back
                    )
                    
                    # Check if meets criteria
                    if (consistency.consistency_score >= min_consistency_score and 
                        consistency.games_analyzed >= 5):
                        
                        # Get current props for this player/stat if available
                        current_prop = self.db.query(NBAPlayerProps).join(NBAPlayer).filter(
                            and_(
                                NBAPlayer.player_id == player.player_id,
                                NBAPlayerProps.prop_type.contains(stat_type.lower())
                            )
                        ).order_by(desc(NBAPlayerProps.last_update)).first()
                        
                        if current_prop:
                            over_rate, under_rate = self.calculate_prop_hit_rates(
                                self.get_player_gamelog_stats(player.player_id, stat_type, days_back),
                                current_prop.line
                            )
                            
                            if over_rate >= min_hit_rate or under_rate >= min_hit_rate:
                                recommendation = {
                                    'player_name': player.name,
                                    'team': player.team_name,
                                    'stat_type': stat_type,
                                    'prop_line': current_prop.line,
                                    'historical_mean': consistency.mean,
                                    'consistency_score': consistency.consistency_score,
                                    'over_hit_rate': over_rate,
                                    'under_hit_rate': under_rate,
                                    'recommended_bet': 'OVER' if over_rate >= min_hit_rate else 'UNDER',
                                    'confidence': max(over_rate, under_rate),
                                    'bookmaker': current_prop.bookmaker,
                                    'over_odds': current_prop.over_odds,
                                    'under_odds': current_prop.under_odds
                                }
                                
                                recommendations['recommendations'].append(recommendation)
                
                except Exception as e:
                    print(f"Error analyzing {player.name} for {stat_type}: {e}")
                    continue
        
        # Sort by confidence
        recommendations['recommendations'].sort(
            key=lambda x: x['confidence'], 
            reverse=True
        )
        
        return recommendations

    def backtest_strategy(self, 
                         stat_type: str,
                         days_back: int = 30,
                         test_period_days: int = 7,
                         min_consistency_score: float = 0.7) -> Dict:
        """
        Backtest the betting strategy over a specific period
        """
        backtest_results = {
            'strategy': {
                'stat_type': stat_type,
                'days_back': days_back,
                'min_consistency_score': min_consistency_score
            },
            'test_period_days': test_period_days,
            'total_bets': 0,
            'winning_bets': 0,
            'losing_bets': 0,
            'win_rate': 0.0,
            'detailed_results': []
        }
        
        # Get players with sufficient data
        cutoff_date = (datetime.now() - timedelta(days=days_back + test_period_days)).strftime('%Y-%m-%d')
        test_start = (datetime.now() - timedelta(days=test_period_days)).strftime('%Y-%m-%d')
        
        players = self.db.query(NBAPlayer).filter(NBAPlayer.team_name.isnot(None)).all()
        
        for player in players:
            try:
                # Get historical data (excluding test period)
                historical_stats = self.db.query(NBAPlayerGamelogs).join(NBAPlayer).filter(
                    and_(
                        NBAPlayer.player_id == player.player_id,
                        NBAPlayerGamelogs.game_date >= cutoff_date,
                        NBAPlayerGamelogs.game_date < test_start
                    )
                ).order_by(desc(NBAPlayerGamelogs.game_date)).all()
                
                if len(historical_stats) < 10:  # Need sufficient historical data
                    continue
                
                # Get test period data
                test_stats = self.db.query(NBAPlayerGamelogs).join(NBAPlayer).filter(
                    and_(
                        NBAPlayer.player_id == player.player_id,
                        NBAPlayerGamelogs.game_date >= test_start
                    )
                ).order_by(desc(NBAPlayerGamelogs.game_date)).all()
                
                if not test_stats:
                    continue
                
                # Calculate historical consistency
                stat_mapping = {
                    'points': 'points',
                    'rebounds': 'rebounds', 
                    'assists': 'assists',
                    'steals': 'steals',
                    'blocks': 'blocks'
                }
                
                if stat_type not in stat_mapping:
                    continue
                
                historical_values = [getattr(log, stat_mapping[stat_type]) 
                                   for log in historical_stats 
                                   if getattr(log, stat_mapping[stat_type]) is not None]
                
                if len(historical_values) < 10:
                    continue
                
                metrics = self.calculate_consistency_metrics(historical_values)
                
                if metrics['consistency_score'] >= min_consistency_score:
                    # Test against actual results
                    for test_log in test_stats:
                        actual_value = getattr(test_log, stat_mapping[stat_type])
                        if actual_value is None:
                            continue
                        
                        predicted_line = metrics['mean']
                        
                        # Simulate betting decision based on consistency
                        if metrics['mean'] > predicted_line + metrics['std_dev'] * 0.3:
                            bet_type = 'OVER'
                            bet_wins = actual_value > predicted_line
                        elif metrics['mean'] < predicted_line - metrics['std_dev'] * 0.3:
                            bet_type = 'UNDER'  
                            bet_wins = actual_value < predicted_line
                        else:
                            continue  # No bet
                        
                        backtest_results['total_bets'] += 1
                        if bet_wins:
                            backtest_results['winning_bets'] += 1
                        else:
                            backtest_results['losing_bets'] += 1
                        
                        backtest_results['detailed_results'].append({
                            'player': player.name,
                            'game_date': test_log.game_date,
                            'predicted_line': predicted_line,
                            'actual_value': actual_value,
                            'bet_type': bet_type,
                            'won': bet_wins,
                            'consistency_score': metrics['consistency_score']
                        })
            
            except Exception as e:
                print(f"Error in backtest for {player.name}: {e}")
                continue
        
        # Calculate win rate
        if backtest_results['total_bets'] > 0:
            backtest_results['win_rate'] = backtest_results['winning_bets'] / backtest_results['total_bets']
        
        return backtest_results


# Usage functions for FastAPI endpoints
def get_algorithm_instance():
    """Get algorithm instance for dependency injection"""
    return NBABettingAlgorithm()


def analyze_prop_bet(player_id: int, stat_type: str, prop_line: float, days_back: int = 30):
    """Convenience function for analyzing a single prop bet"""
    with NBABettingAlgorithm() as algo:
        return algo.analyze_prop_value(player_id, stat_type, prop_line, days_back)


def get_consistent_players(stat_type: str, top_n: int = 20, days_back: int = 30):
    """Convenience function for getting most consistent players"""
    with NBABettingAlgorithm() as algo:
        return algo.find_most_consistent_players(stat_type, days_back=days_back, top_n=top_n)


def populate_gamelogs_for_team(team_name: str, max_players: int = 10):
    """Convenience function for populating gamelogs for a team"""
    with NBABettingAlgorithm() as algo:
        return algo.bulk_populate_gamelogs(team_name=team_name, max_players=max_players)


def get_daily_recommendations(min_consistency: float = 0.7, min_hit_rate: float = 0.6):
    """Convenience function for getting daily prop recommendations"""
    with NBABettingAlgorithm() as algo:
        return algo.get_daily_prop_recommendations(
            min_consistency_score=min_consistency,
            min_hit_rate=min_hit_rate
        )


def run_backtest(stat_type: str, days_back: int = 30, test_period: int = 7):
    """Convenience function for running strategy backtest"""
    with NBABettingAlgorithm() as algo:
        return algo.backtest_strategy(
            stat_type=stat_type,
            days_back=days_back,
            test_period_days=test_period
        )



