"use client";

import { useState, useEffect } from "react";
import { Play, Pause, Square } from "lucide-react";

interface TimerProps {
  onTimeEntry?: (duration: number, description?: string) => void;
  initialDuration?: number; // in seconds
}

export default function Timer({ onTimeEntry, initialDuration = 0 }: TimerProps) {
  const [isRunning, setIsRunning] = useState(false);
  const [duration, setDuration] = useState(initialDuration);
  const [description, setDescription] = useState("");

  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;

    if (isRunning) {
      interval = setInterval(() => {
        setDuration((prev) => prev + 1);
      }, 1000);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isRunning]);

  const formatTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
    }
    return `${minutes.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };

  const handleStart = () => {
    setIsRunning(true);
  };

  const handlePause = () => {
    setIsRunning(false);
  };

  const handleStop = () => {
    setIsRunning(false);
    if (onTimeEntry && duration > 0) {
      onTimeEntry(duration, description);
    }
    setDuration(0);
    setDescription("");
  };

  return (
    <div className="bg-white border border-slate-200 rounded-lg p-4 shadow-sm">
      {/* Timer display */}
      <div className="text-center mb-4">
        <div className="text-4xl font-mono font-semibold text-slate-900">
          {formatTime(duration)}
        </div>
        <p className="text-sm text-slate-500 mt-1">
          {isRunning ? "Timer running" : duration > 0 ? "Timer paused" : "Ready to start"}
        </p>
      </div>

      {/* Description input */}
      <input
        type="text"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="What are you working on?"
        className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-sky-500 mb-4"
        disabled={isRunning}
      />

      {/* Controls */}
      <div className="flex items-center gap-2">
        {!isRunning ? (
          <button
            onClick={handleStart}
            disabled={duration === 0 && !description}
            className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-sky-600 text-white rounded-lg hover:bg-sky-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Play className="w-4 h-4" />
            Start
          </button>
        ) : (
          <button
            onClick={handlePause}
            className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-amber-500 text-white rounded-lg hover:bg-amber-600 transition-colors"
          >
            <Pause className="w-4 h-4" />
            Pause
          </button>
        )}
        <button
          onClick={handleStop}
          disabled={duration === 0}
          className="flex items-center justify-center gap-2 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <Square className="w-4 h-4" />
          Stop
        </button>
      </div>
    </div>
  );
}
