import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const Home: React.FC = () => {
  const [url, setUrl] = useState('');
  const [whitelist, setWhitelist] = useState<string[]>([]);
  const [blacklist, setBlacklist] = useState<string[]>([]);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [selectedTool, setSelectedTool] = useState<string>('scrape'); // Default to 'scrape'
  const navigate = useNavigate();

  const handleScrape = async () => {
    setLoading(true);
    try {
      let response;
      switch (selectedTool) {
        case 'scrape':
          response = await api.post('/scrape/', {
            url,
            whitelist,
            blacklist,
          });
          break;
        case 'scrape_single_page':
          response = await api.post('/scrape_single_page/', { url });
          break;
        case 'single_page_media':
          response = await api.post('/single_page_media/', { url });
          break;
        case 'multiple_page_media':
          response = await api.post('/multiple_page_media/', {
            url,
            whitelist,
            blacklist,
          });
          break;
        default:
          throw new Error('Invalid tool selected');
      }
      setResult(response.data);
      setError(null);
    } catch (err) {
      console.error(err);
      setError('An error occurred during scraping.');
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const handleFetch = async () => {
    setLoading(true);
    try {
      const response = await api.get('/fetch/', {
        params: { url },
      });
      setError(null);
      navigate('/result', { state: { data: response.data } });
    } catch (err) {
      console.error(err);
      setError('An error occurred while fetching data.');
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Web Scraper</h1>
      <div style={styles.form}>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter URL"
          style={styles.input as React.CSSProperties}
        />
        <input
          type="text"
          value={whitelist.join(', ')}
          onChange={(e) =>
            setWhitelist(e.target.value.split(',').map((item) => item.trim()))
          }
          placeholder="Enter whitelist (comma-separated)"
          style={styles.input as React.CSSProperties}
        />
        <input
          type="text"
          value={blacklist.join(', ')}
          onChange={(e) =>
            setBlacklist(e.target.value.split(',').map((item) => item.trim()))
          }
          placeholder="Enter blacklist (comma-separated)"
          style={styles.input as React.CSSProperties}
        />

        {/* Tool Selection */}
        <div style={styles.checkboxContainer as React.CSSProperties}>
          <label style={styles.checkboxLabel as React.CSSProperties}>
            <input
              type="radio"
              value="scrape"
              checked={selectedTool === 'scrape'}
              onChange={() => setSelectedTool('scrape')}
            />
            Scrape
          </label>
          <label style={styles.checkboxLabel as React.CSSProperties}>
            <input
              type="radio"
              value="scrape_single_page"
              checked={selectedTool === 'scrape_single_page'}
              onChange={() => setSelectedTool('scrape_single_page')}
            />
            Scrape Single Page
          </label>
          <label style={styles.checkboxLabel as React.CSSProperties}>
            <input
              type="radio"
              value="single_page_media"
              checked={selectedTool === 'single_page_media'}
              onChange={() => setSelectedTool('single_page_media')}
            />
            Single Page Media
          </label>
          <label style={styles.checkboxLabel as React.CSSProperties}>
            <input
              type="radio"
              value="multiple_page_media"
              checked={selectedTool === 'multiple_page_media'}
              onChange={() => setSelectedTool('multiple_page_media')}
            />
            Multiple Page Media
          </label>
        </div>

        <div style={styles.buttonContainer as React.CSSProperties}>
          <button onClick={handleScrape} style={styles.button as React.CSSProperties} disabled={loading}>
            Scrape
          </button>
          <button onClick={handleFetch} style={styles.button as React.CSSProperties} disabled={loading}>
            Fetch
          </button>
        </div>
      </div>
      {loading && <p style={styles.loading as React.CSSProperties}>Loading...</p>}
      {error && <p style={styles.error as React.CSSProperties}>{error}</p>}
      {result && !error && !window.location.search.includes('data') && (
        <div style={styles.result as React.CSSProperties}>
          <h2 style={styles.resultTitle as React.CSSProperties}>Scraped Content:</h2>
          <pre style={styles.pre as React.CSSProperties}>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

// Styles object
const styles: { [key: string]: React.CSSProperties } = {
  container: {
    padding: '20px',
    maxWidth: '800px',
    margin: 'auto',
    backgroundColor: '#f4f4f4',
    borderRadius: '8px',
    boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
  },
  title: {
    textAlign: 'center',
    color: '#333',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
  },
  input: {
    padding: '10px',
    fontSize: '16px',
    borderRadius: '4px',
    border: '1px solid #ddd',
    outline: 'none',
    width: '100%',
  },
  buttonContainer: {
    display: 'flex',
    gap: '10px',
    justifyContent: 'center',
  },
  button: {
    padding: '10px 20px',
    fontSize: '16px',
    borderRadius: '4px',
    border: 'none',
    backgroundColor: '#007bff',
    color: '#fff',
    cursor: 'pointer',
    transition: 'background-color 0.3s',
  },
  error: {
    color: 'red',
    textAlign: 'center',
    marginTop: '20px',
  },
  result: {
    marginTop: '20px',
    backgroundColor: '#fff',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
  },
  resultTitle: {
    marginBottom: '10px',
    color: '#333',
  },
  pre: {
    backgroundColor: '#f4f4f4',
    padding: '10px',
    borderRadius: '4px',
    overflowX: 'auto',
  },
  loading: {
    textAlign: 'center',
    color: '#007bff',
    marginTop: '20px',
  },
  checkboxContainer: {
    display: 'flex',
    gap: '10px',
    justifyContent: 'center',
    marginTop: '10px',
  },
  checkboxLabel: {
    fontSize: '14px',
  },
};

export default Home;
