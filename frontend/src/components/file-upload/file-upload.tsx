"use client";

import { useState, useRef } from "react";
import { Upload, X, File as FileIcon } from "lucide-react";

interface FileUploadProps {
  onUpload: (files: File[]) => void;
  accept?: string;
  multiple?: boolean;
  maxSize?: number; // in bytes
  maxFiles?: number;
}

export default function FileUpload({
  onUpload,
  accept = "*/*",
  multiple = false,
  maxSize = 10 * 1024 * 1024, // 10MB default
  maxFiles = 5,
}: FileUploadProps) {
  const [dragActive, setDragActive] = useState(false);
  const [files, setFiles] = useState<File[]>([]);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const droppedFiles = Array.from(e.dataTransfer.files);
    validateAndSetFiles(droppedFiles);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files);
      validateAndSetFiles(selectedFiles);
    }
  };

  const validateAndSetFiles = (newFiles: File[]) => {
    setError(null);

    // Check max files
    if (files.length + newFiles.length > maxFiles) {
      setError(`Maximum ${maxFiles} files allowed`);
      return;
    }

    // Validate each file
    const validFiles: File[] = [];
    for (const file of newFiles) {
      if (file.size > maxSize) {
        setError(`File ${file.name} exceeds maximum size of ${maxSize / 1024 / 1024}MB`);
        return;
      }
      validFiles.push(file);
    }

    setFiles([...files, ...validFiles]);
  };

  const removeFile = (index: number) => {
    setFiles(files.filter((_, i) => i !== index));
  };

  const handleUpload = () => {
    if (files.length > 0) {
      onUpload(files);
      setFiles([]);
      setError(null);
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + " " + sizes[i];
  };

  return (
    <div className="w-full">
      {/* Drop zone */}
      <div
        className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          dragActive
            ? "border-sky-500 bg-sky-50"
            : "border-slate-300 hover:border-sky-400"
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          ref={inputRef}
          type="file"
          className="hidden"
          accept={accept}
          multiple={multiple}
          onChange={handleChange}
        />
        
        <Upload className="w-12 h-12 mx-auto text-slate-400 mb-4" />
        <p className="text-sm text-slate-600 mb-2">
          Drag and drop files here, or{" "}
          <button
            onClick={() => inputRef.current?.click()}
            className="text-sky-600 hover:text-sky-700 font-medium"
          >
            browse
          </button>
        </p>
        <p className="text-xs text-slate-500">
          Maximum {maxFiles} files, {maxSize / 1024 / 1024}MB each
        </p>
      </div>

      {/* Error message */}
      {error && (
        <div className="mt-2 text-sm text-red-600">{error}</div>
      )}

      {/* File list */}
      {files.length > 0 && (
        <div className="mt-4 space-y-2">
          {files.map((file, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-3 bg-slate-50 rounded-lg"
            >
              <div className="flex items-center gap-3 flex-1 min-w-0">
                <FileIcon className="w-5 h-5 text-slate-400 flex-shrink-0" />
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium text-slate-900 truncate">
                    {file.name}
                  </p>
                  <p className="text-xs text-slate-500">
                    {formatFileSize(file.size)}
                  </p>
                </div>
              </div>
              <button
                onClick={() => removeFile(index)}
                className="p-1 text-slate-400 hover:text-red-600 transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          ))}

          {/* Upload button */}
          <button
            onClick={handleUpload}
            className="w-full mt-3 px-4 py-2 bg-sky-600 text-white rounded-lg hover:bg-sky-700 transition-colors"
          >
            Upload {files.length} file{files.length !== 1 ? "s" : ""}
          </button>
        </div>
      )}
    </div>
  );
}
