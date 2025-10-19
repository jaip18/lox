"use client";

import { Card } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Calendar } from "@/components/ui/calendar";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Button } from "@/components/ui/button";
import { CalendarIcon } from "lucide-react";
import { format } from "date-fns";
import { useState } from "react";

interface FilterPanelProps {
  onFiltersChange?: (filters: any) => void;
}

export const FilterPanel = ({ onFiltersChange }: FilterPanelProps) => {
  const [confidence, setConfidence] = useState([70]);
  const [date, setDate] = useState<Date>();

  return (
    <Card className="h-fit border-border bg-card p-6">
      <h2 className="mb-6 text-lg font-semibold">Filters</h2>

      <div className="space-y-6">
        <div className="space-y-3">
          <Label>Confidence Score</Label>
          <div className="flex items-center gap-3">
            <Slider
              value={confidence}
              onValueChange={setConfidence}
              max={100}
              step={5}
              className="flex-1"
            />
            <span className="w-12 text-right text-sm font-medium text-primary">
              {confidence}%+
            </span>
          </div>
        </div>

        <div className="space-y-3">
          <Label>Bet Type</Label>
          <Select defaultValue="all">
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Types</SelectItem>
              <SelectItem value="points">Points</SelectItem>
              <SelectItem value="rebounds">Rebounds</SelectItem>
              <SelectItem value="assists">Assists</SelectItem>
              <SelectItem value="threes">3-Pointers</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-3">
          <Label>Position</Label>
          <Select defaultValue="all">
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Positions</SelectItem>
              <SelectItem value="pg">Point Guard</SelectItem>
              <SelectItem value="sg">Shooting Guard</SelectItem>
              <SelectItem value="sf">Small Forward</SelectItem>
              <SelectItem value="pf">Power Forward</SelectItem>
              <SelectItem value="c">Center</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-3">
          <Label>Game Date</Label>
          <Popover>
            <PopoverTrigger asChild>
              <Button
                variant="outline"
                className="w-full justify-start text-left font-normal"
              >
                <CalendarIcon className="mr-2 h-4 w-4" />
                {date ? format(date, "PPP") : "Select date"}
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-auto p-0" align="start">
              <Calendar
                mode="single"
                selected={date}
                onSelect={setDate}
                initialFocus
              />
            </PopoverContent>
          </Popover>
        </div>
      </div>
    </Card>
  );
};
