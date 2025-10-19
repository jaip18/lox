import { Card } from "@/components/ui/card";
import { AlertCircle, TrendingUp, Database, Shield } from "lucide-react";

const About = () => {
  return (
    <div className="container py-8">
      <div className="mx-auto max-w-4xl space-y-8">
        <div className="text-center">
          <h1 className="mb-4 text-4xl font-bold bg-gradient-primary bg-clip-text text-transparent">
            About PropEdge
          </h1>
          <p className="text-lg text-muted-foreground">
            AI-powered NBA player prop analytics
          </p>
        </div>

        <Card className="border-border bg-gradient-card p-8">
          <div className="space-y-6">
            <div>
              <h2 className="mb-3 text-2xl font-semibold flex items-center gap-2">
                <TrendingUp className="h-6 w-6 text-primary" />
                Our Mission
              </h2>
              <p className="text-muted-foreground leading-relaxed">
                PropEdge leverages advanced analytics and machine learning to provide data-driven
                insights for NBA player prop bets. We analyze historical performance, matchup data,
                team dynamics, and real-time factors to generate confidence scores for prop bet opportunities.
              </p>
            </div>

            <div>
              <h2 className="mb-3 text-2xl font-semibold flex items-center gap-2">
                <Database className="h-6 w-6 text-primary" />
                How It Works
              </h2>
              <p className="text-muted-foreground leading-relaxed">
                Our algorithm analyzes multiple data points including:
              </p>
              <ul className="mt-3 space-y-2 text-muted-foreground">
                <li className="flex items-start gap-2">
                  <span className="mt-1 h-1.5 w-1.5 rounded-full bg-primary flex-shrink-0" />
                  Player performance trends and historical statistics
                </li>
                <li className="flex items-start gap-2">
                  <span className="mt-1 h-1.5 w-1.5 rounded-full bg-primary flex-shrink-0" />
                  Opponent defensive ratings and matchup history
                </li>
                <li className="flex items-start gap-2">
                  <span className="mt-1 h-1.5 w-1.5 rounded-full bg-primary flex-shrink-0" />
                  Recent form, injuries, and lineup changes
                </li>
                <li className="flex items-start gap-2">
                  <span className="mt-1 h-1.5 w-1.5 rounded-full bg-primary flex-shrink-0" />
                  Home/away splits and back-to-back game factors
                </li>
              </ul>
            </div>

            <div>
              <h2 className="mb-3 text-2xl font-semibold flex items-center gap-2">
                <Shield className="h-6 w-6 text-primary" />
                Data Sources
              </h2>
              <p className="text-muted-foreground leading-relaxed">
                We pull data from official NBA APIs, verified statistics providers, and reputable
                sports data aggregators. All data is updated in real-time to ensure accuracy.
              </p>
            </div>
          </div>
        </Card>

        <Card className="border-destructive/50 bg-destructive/5 p-6">
          <div className="flex gap-4">
            <AlertCircle className="h-6 w-6 text-destructive flex-shrink-0" />
            <div>
              <h3 className="mb-2 font-semibold text-destructive">Important Disclaimer</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                PropEdge is for informational and entertainment purposes only. We do not guarantee
                the accuracy of predictions or recommend any specific betting actions. Sports betting
                involves risk and may not be legal in your jurisdiction. Always gamble responsibly
                and never bet more than you can afford to lose. Confidence scores represent
                algorithmic probability estimates and should not be considered financial advice.
              </p>
            </div>
          </div>
        </Card>

        <div className="text-center text-sm text-muted-foreground">
          <p>Data accuracy and freshness may vary. Last updated: Real-time</p>
        </div>
      </div>
    </div>
  );
};

export default About;
