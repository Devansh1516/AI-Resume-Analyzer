import { useCallback, useMemo, useRef, useState } from "react";
import {
  CloudUpload,
  FileText,
  LoaderCircle,
  Sparkles,
  X,
} from "lucide-react";

function ResumeUpload({ onAnalyze, isLoading }) {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [isDragging, setIsDragging] = useState(false);

  const inputRef = useRef(null);

  const fileLabel = useMemo(() => {
    if (!file) return "PDF up to 8 MB";
    return `${file.name} - ${(file.size / 1024 / 1024).toFixed(2)} MB`;
  }, [file]);

  const acceptFile = useCallback(
    (candidate) => {
      if (!candidate) return;

      if (candidate.type !== "application/pdf") {
        onAnalyze(null, "", "Please upload a PDF resume.");
        return;
      }

      setFile(candidate);
    },
    [onAnalyze]
  );

  const handleDrop = (event) => {
    event.preventDefault();
    setIsDragging(false);

    acceptFile(event.dataTransfer.files?.[0]);
  };

  const handleSubmit = () => {
    if (!jobDescription.trim()) {
      onAnalyze(file, jobDescription, "Paste the job description before analyzing.");
      return;
    }

    onAnalyze(file, jobDescription, null);
  };

  return (
    <section id="upload" className="upload-card">
      <div className="section-kicker">
        <Sparkles size={16} />
        Resume intelligence
      </div>

      <h2>Upload a resume PDF</h2>

      <p>
        Get a job-specific match score, matching skills,
        missing keywords, selection probability,
        and practical edits in one pass.
      </p>

      <button
        type="button"
        className={`dropzone ${
          isDragging ? "is-dragging" : ""
        }`}
        onClick={() => inputRef.current?.click()}
        onDragOver={(event) => {
          event.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
      >
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          onChange={(event) =>
            acceptFile(event.target.files?.[0])
          }
          hidden
        />

        <span className="upload-icon">
          <CloudUpload size={34} />
        </span>

        <strong>
          Drag and drop your PDF here
        </strong>

        <span>{fileLabel}</span>
      </button>

      {file && (
        <div className="selected-file">
          <FileText size={18} />

          <span>{file.name}</span>

          <button
            type="button"
            onClick={() => setFile(null)}
            aria-label="Remove selected file"
          >
            <X size={16} />
          </button>
        </div>
      )}

      <div className="job-description-section">
        <label htmlFor="jobDescription">
          Job Description
        </label>

        <textarea
          id="jobDescription"
          className="job-description-textarea"
          placeholder="Paste the complete job description here..."
          value={jobDescription}
          onChange={(e) =>
            setJobDescription(e.target.value)
          }
          rows={8}
        />
      </div>

      <button
        className="primary-button"
        type="button"
        onClick={handleSubmit}
        disabled={isLoading}
      >
        {isLoading ? (
          <>
            <LoaderCircle
              className="spin"
              size={20}
            />
            Analyzing Resume
          </>
        ) : (
          <>
            <Sparkles size={20} />
            Analyze Resume
          </>
        )}
      </button>
    </section>
  );
}

export default ResumeUpload;
