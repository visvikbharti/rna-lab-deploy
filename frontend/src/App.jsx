import { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import ChatBox from './components/ChatBox';
import EnhancedChatBox from './components/EnhancedChatBox';
import AdvancedSearchBox from './components/AdvancedSearchBox';
import FilterChips from './components/FilterChips';
import ProtocolUploader from './components/ProtocolUploader';
import { FeedbackAnalyticsDashboard } from './components/feedback';
import SearchQualityDashboard from './components/SearchQualityDashboard';
import SecurityAuditDashboard from './components/SecurityAuditDashboard';
import './App.css';

function MainApp() {
  const [docType, setDocType] = useState('all');

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <header className="mb-8 text-center">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">RNA Lab Navigator</h1>
        <p className="text-gray-600">
          Your AI assistant for lab protocols, papers, and theses
        </p>
        
        <nav className="mt-4">
          <ul className="flex justify-center space-x-6">
            <li>
              <Link to="/" className="text-primary-600 hover:text-primary-800 font-medium">
                Home
              </Link>
            </li>
            <li>
              <Link to="/upload" className="text-primary-600 hover:text-primary-800 font-medium">
                Upload Protocol
              </Link>
            </li>
            <li>
              <Link to="/analytics" className="text-primary-600 hover:text-primary-800 font-medium">
                Feedback Analytics
              </Link>
            </li>
            <li>
              <Link to="/search-quality" className="text-primary-600 hover:text-primary-800 font-medium">
                Search Quality
              </Link>
            </li>
            <li>
              <Link to="/security" className="text-primary-600 hover:text-primary-800 font-medium">
                Security Audit
              </Link>
            </li>
          </ul>
        </nav>
      </header>

      <main>
        <FilterChips selected={docType} onChange={setDocType} />
        <AdvancedSearchBox docType={docType} />
      </main>

      <footer className="mt-12 text-center text-gray-500 text-sm">
        <p>© 2025 Dr. Debojyoti Chakraborty's RNA Biology Lab (CSIR-IGIB)</p>
      </footer>
    </div>
  );
}

function UploadPage() {
  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <header className="mb-8 text-center">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">RNA Lab Navigator</h1>
        <p className="text-gray-600">
          Upload Protocol Documents
        </p>
        
        <nav className="mt-4">
          <ul className="flex justify-center space-x-6">
            <li>
              <Link to="/" className="text-primary-600 hover:text-primary-800 font-medium">
                Home
              </Link>
            </li>
            <li>
              <Link to="/upload" className="text-gray-800 font-bold">
                Upload Protocol
              </Link>
            </li>
            <li>
              <Link to="/analytics" className="text-primary-600 hover:text-primary-800 font-medium">
                Feedback Analytics
              </Link>
            </li>
            <li>
              <Link to="/search-quality" className="text-primary-600 hover:text-primary-800 font-medium">
                Search Quality
              </Link>
            </li>
            <li>
              <Link to="/security" className="text-primary-600 hover:text-primary-800 font-medium">
                Security Audit
              </Link>
            </li>
          </ul>
        </nav>
      </header>

      <main>
        <ProtocolUploader />
      </main>

      <footer className="mt-12 text-center text-gray-500 text-sm">
        <p>© 2025 Dr. Debojyoti Chakraborty's RNA Biology Lab (CSIR-IGIB)</p>
      </footer>
    </div>
  );
}

function AnalyticsPage() {
  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      <header className="mb-8 text-center">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">RNA Lab Navigator</h1>
        <p className="text-gray-600">
          Feedback Analytics Dashboard
        </p>
        
        <nav className="mt-4">
          <ul className="flex justify-center space-x-6">
            <li>
              <Link to="/" className="text-primary-600 hover:text-primary-800 font-medium">
                Home
              </Link>
            </li>
            <li>
              <Link to="/upload" className="text-primary-600 hover:text-primary-800 font-medium">
                Upload Protocol
              </Link>
            </li>
            <li>
              <Link to="/analytics" className="text-gray-800 font-bold">
                Feedback Analytics
              </Link>
            </li>
            <li>
              <Link to="/search-quality" className="text-primary-600 hover:text-primary-800 font-medium">
                Search Quality
              </Link>
            </li>
            <li>
              <Link to="/security" className="text-primary-600 hover:text-primary-800 font-medium">
                Security Audit
              </Link>
            </li>
          </ul>
        </nav>
      </header>

      <main>
        <FeedbackAnalyticsDashboard />
      </main>

      <footer className="mt-12 text-center text-gray-500 text-sm">
        <p>© 2025 Dr. Debojyoti Chakraborty's RNA Biology Lab (CSIR-IGIB)</p>
      </footer>
    </div>
  );
}

function SearchQualityPage() {
  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      <header className="mb-8 text-center">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">RNA Lab Navigator</h1>
        <p className="text-gray-600">
          Search Quality Dashboard
        </p>
        
        <nav className="mt-4">
          <ul className="flex justify-center space-x-6">
            <li>
              <Link to="/" className="text-primary-600 hover:text-primary-800 font-medium">
                Home
              </Link>
            </li>
            <li>
              <Link to="/upload" className="text-primary-600 hover:text-primary-800 font-medium">
                Upload Protocol
              </Link>
            </li>
            <li>
              <Link to="/analytics" className="text-primary-600 hover:text-primary-800 font-medium">
                Feedback Analytics
              </Link>
            </li>
            <li>
              <Link to="/search-quality" className="text-gray-800 font-bold">
                Search Quality
              </Link>
            </li>
          </ul>
        </nav>
      </header>

      <main>
        <SearchQualityDashboard />
      </main>

      <footer className="mt-12 text-center text-gray-500 text-sm">
        <p>© 2025 Dr. Debojyoti Chakraborty's RNA Biology Lab (CSIR-IGIB)</p>
      </footer>
    </div>
  );
}

function SecurityAuditPage() {
  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl">
      <header className="mb-8 text-center">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">RNA Lab Navigator</h1>
        <p className="text-gray-600">
          Security Audit Dashboard
        </p>
        
        <nav className="mt-4">
          <ul className="flex justify-center space-x-6">
            <li>
              <Link to="/" className="text-primary-600 hover:text-primary-800 font-medium">
                Home
              </Link>
            </li>
            <li>
              <Link to="/upload" className="text-primary-600 hover:text-primary-800 font-medium">
                Upload Protocol
              </Link>
            </li>
            <li>
              <Link to="/analytics" className="text-primary-600 hover:text-primary-800 font-medium">
                Feedback Analytics
              </Link>
            </li>
            <li>
              <Link to="/search-quality" className="text-primary-600 hover:text-primary-800 font-medium">
                Search Quality
              </Link>
            </li>
            <li>
              <Link to="/security" className="text-gray-800 font-bold">
                Security Audit
              </Link>
            </li>
          </ul>
        </nav>
      </header>

      <main>
        <SecurityAuditDashboard />
      </main>

      <footer className="mt-12 text-center text-gray-500 text-sm">
        <p>© 2025 Dr. Debojyoti Chakraborty's RNA Biology Lab (CSIR-IGIB)</p>
      </footer>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainApp />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/analytics" element={<AnalyticsPage />} />
        <Route path="/search-quality" element={<SearchQualityPage />} />
        <Route path="/security" element={<SecurityAuditPage />} />
      </Routes>
    </Router>
  );
}

export default App;