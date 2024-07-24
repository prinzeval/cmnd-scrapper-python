import React, { useState } from "react";
import api from "../api"; // Adjust this import path based on your project structure

const Home: React.FC = () => {
  const [url, setUrl] = useState("");
  const [whitelist, setWhitelist] = useState<string[]>([]);
  const [blacklist, setBlacklist] = useState<string[]>([]);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  // Function to handle the scraping request
  const handleScrape = async () => {
    try {
      const response = await api.post("/scrape/", {
        url,
        whitelist,
        blacklist,
      });
      setResult(response.data);
      setError(null);
    } catch (err) {
      setError("An error occurred during scraping.");
      setResult(null);
    }
  };

  // Function to handle the fetch request
  const handleFetch = async () => {
    try {
      const response = await api.get(`/fetch/`, {
        params: { url },
      });
      setResult(response.data);
      setError(null);
    } catch (err) {
      setError("An error occurred while fetching data.");
      setResult(null);
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
          style={styles.input}
        />
        <input
          type="text"
          value={whitelist.join(", ")}
          onChange={(e) =>
            setWhitelist(e.target.value.split(",").map((item) => item.trim()))
          }
          placeholder="Enter whitelist (comma-separated)"
          style={styles.input}
        />
        <input
          type="text"
          value={blacklist.join(", ")}
          onChange={(e) =>
            setBlacklist(e.target.value.split(",").map((item) => item.trim()))
          }
          placeholder="Enter blacklist (comma-separated)"
          style={styles.input}
        />
        <div style={styles.buttonContainer}>
          <button onClick={handleScrape} style={styles.button}>
            Scrape
          </button>
          <button onClick={handleFetch} style={styles.button}>
            Fetch
          </button>
        </div>
      </div>
      {error && <p style={styles.error}>{error}</p>}
      {result && (
        <div style={styles.result}>
          <h2 style={styles.resultTitle}>Result:</h2>
          <pre style={styles.pre}>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

// Styles object
const styles = {
  container: {
    padding: "20px",
    maxWidth: "800px",
    margin: "auto",
    backgroundColor: "#f4f4f4",
    borderRadius: "8px",
    boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)",
  },
  title: {
    textAlign: "center",
    color: "#333",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  input: {
    padding: "10px",
    fontSize: "16px",
    borderRadius: "4px",
    border: "1px solid #ddd",
    outline: "none",
    width: "100%",
  },
  buttonContainer: {
    display: "flex",
    gap: "10px",
    justifyContent: "center",
  },
  button: {
    padding: "10px 20px",
    fontSize: "16px",
    borderRadius: "4px",
    border: "none",
    backgroundColor: "#007bff",
    color: "#fff",
    cursor: "pointer",
    transition: "background-color 0.3s",
  },
  buttonHover: {
    backgroundColor: "#0056b3",
  },
  error: {
    color: "red",
    textAlign: "center",
    marginTop: "20px",
  },
  result: {
    marginTop: "20px",
    backgroundColor: "#fff",
    padding: "20px",
    borderRadius: "8px",
    boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)",
  },
  resultTitle: {
    marginBottom: "10px",
    color: "#333",
  },
  pre: {
    backgroundColor: "#f4f4f4",
    padding: "10px",
    borderRadius: "4px",
    overflowX: "auto",
  },
};

export default Home;
