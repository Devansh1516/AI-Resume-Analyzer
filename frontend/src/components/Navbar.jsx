import { ExternalLink, FileScan } from "lucide-react";
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <header className="navbar">
      <Link to="/" className="brand" aria-label="AI Resume Analyzer home">
        <span className="brand-icon">
          <FileScan size={22} />
        </span>
        <span>AI Resume Analyzer</span>
      </Link>
    </header>
  );
}

export default Navbar;
