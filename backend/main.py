from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import crud
import apis.nba_api_utils
import apis.odds_api
from models import NBAPlayer
import time
from datetime import datetime, timezone

today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT00:00:00Z")

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def load_initial_data():
    print("🚀 Starting data load...")

    db: Session = next(get_db())  # Use your defined DB dependency

    try:
        players = apis.nba_api_utils.fetch_active_players()
        print(f"Fetched {len(players)} active players")

        for player in players:
            try:
                id = player['id']
                existing_player = db.query(NBAPlayer).filter_by(player_id=id).first()
                if existing_player:
                    time.sleep(5)
                    player_data = apis.nba_api_utils.fetch_player_info(id)
                    player_stats = apis.nba_api_utils.fetch_player_stats(id)
                    crud.update_NBAplayer(db, player_data, player_stats)
                else:
                    time.sleep(5)
                    player_data = apis.nba_api_utils.fetch_player_info(id)
                    player_stats = apis.nba_api_utils.fetch_player_stats(id)
                    crud.create_NBAplayer(db, player_data, player_stats)

            except Exception as e:
                print(f"⚠️ Error processing player {id}: {e}")

    finally:
        db.close()
        print("✅ DB session closed after initial load")



    
    

