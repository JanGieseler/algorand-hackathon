import React, { useState, useCallback } from "react";

interface JsonDropzoneProps {
  onJsonParsed: (data: any) => void;
}

const JsonDropzone: React.FC<JsonDropzoneProps> = ({ onJsonParsed }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [dropState, setDropState] = useState<"idle" | "success" | "error">("idle");

  const handleDragEnter = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setDropState("idle"); // Reset on new drag
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragging(false);

      const files = e.dataTransfer.files;
      const resetDropState = () => setTimeout(() => setDropState("idle"), 2000);

      if (files && files.length > 0) {
        const file = files[0];
        if (file.type === "application/json") {
          const reader = new FileReader();
          reader.onload = (event) => {
            try {
              if (event.target && typeof event.target.result === "string") {
                const json = JSON.parse(event.target.result);
                onJsonParsed(json);
                setDropState("success");
                resetDropState();
              } else {
                throw new Error("Failed to read file");
              }
            } catch (error) {
              console.error("Error parsing JSON file:", error);
              setDropState("error");
              resetDropState();
            }
          };
          reader.onerror = () => {
            console.error("Error reading file");
            setDropState("error");
            resetDropState();
          };
          reader.readAsText(file);
        } else {
          console.error("Invalid file type. Please drop a JSON file.");
          setDropState("error");
          resetDropState();
        }
      }
    },
    [onJsonParsed]
  );

  const getDropzoneClassName = () => {
    if (isDragging) {
      return "border-teal-500 bg-teal-50 ring-4 ring-teal-200";
    }
    if (dropState === "success") {
      return "border-green-500 bg-green-50 ring-4 ring-green-200";
    }
    if (dropState === "error") {
      return "border-red-500 bg-red-50 ring-4 ring-red-200";
    }
    return "border-gray-300 hover:border-gray-400";
  };

  const getDropzoneContent = () => {
    if (isDragging) {
      return <p className="text-teal-700 font-semibold">Drop the file to populate the form</p>;
    }
    if (dropState === "success") {
      return <p className="text-green-700 font-semibold">✅ File parsed successfully!</p>;
    }
    if (dropState === "error") {
      return <p className="text-red-700 font-semibold">❌ Invalid file. Please drop a valid JSON file.</p>;
    }
    return <p className="text-gray-500">Drag and drop a JSON file here, or click to select a file.</p>;
  };

  return (
    <div
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragEnter={handleDragEnter}
      onDragLeave={handleDragLeave}
      className={`border-2 border-dashed rounded-lg p-8 text-center transition-all duration-300 ${getDropzoneClassName()}`}
    >
      {getDropzoneContent()}
      {/* You can also add a hidden file input to allow clicking to select files */}
      {/* <input type="file" accept=".json" className="hidden" /> */}
    </div>
  );
};

export default JsonDropzone;
