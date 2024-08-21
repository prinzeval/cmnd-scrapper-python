import React from "react";
import { useLocation } from "react-router-dom";

interface MediaLinksProps {
  media_links: string;
}

const MediaLinks: React.FC<MediaLinksProps> = ({ media_links }) => {
  const links = media_links.split(",").map((link) => link.trim());
  return (
    <div style={styles.mediaLinks as React.CSSProperties}>
      <strong>Media Links:</strong>
      {links.length > 0 ? (
        <ul style={styles.linkList as React.CSSProperties}>
          {links.map((link, index) => (
            <li key={index} style={styles.linkItem as React.CSSProperties}>
              <a
                href={link}
                target="_blank"
                rel="noopener noreferrer"
                style={styles.link as React.CSSProperties}
              >
                {link}
              </a>
            </li>
          ))}
        </ul>
      ) : (
        <p>No media links available.</p>
      )}
    </div>
  );
};

const Result: React.FC = () => {
  const location = useLocation();
  const { data } = location.state as { data: any[] }; // Expecting an array

  console.log("Received data:", data);

  if (!data || data.length === 0) {
    return <div>No data available</div>;
  }

  return (
    <div style={styles.container as React.CSSProperties}>
      <h1 style={styles.title as React.CSSProperties}>Fetch Result</h1>
      {data.map((item: any, index: number) => {
        const { title, content, media_links, url } = item;
        return (
          <div key={index} style={styles.result as React.CSSProperties}>
            <h2 style={styles.resultTitle as React.CSSProperties}>{title || "No Title"}</h2>
            <p>
              <strong>Content:</strong>
            </p>
            <pre style={styles.pre as React.CSSProperties}>{content || "No Content"}</pre>
            <p>
              <strong>Source URL:</strong>{" "}
              <a
                href={url}
                target="_blank"
                rel="noopener noreferrer"
                style={styles.link as React.CSSProperties}
              >
                {url}
              </a>
            </p>
            <MediaLinks media_links={media_links || ""} />
          </div>
        );
      })}
    </div>
  );
};

// Styles object
const styles: { [key: string]: React.CSSProperties } = {
  container: {
    padding: "20px",
    maxWidth: "600px",
    margin: "auto",
    backgroundColor: "#ffffffcc", // Semi-transparent white background
    borderRadius: "8px",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
    backdropFilter: "blur(10px)", // Blurring background behind the container
    fontFamily: "Arial, sans-serif",
  },
  title: {
    textAlign: "center",
    color: "#333",
    fontSize: "24px",
    marginBottom: "20px",
  },
  result: {
    backgroundColor: "#f8f9fa",
    padding: "20px",
    borderRadius: "8px",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
    marginBottom: "20px",
  },
  resultTitle: {
    marginBottom: "15px",
    color: "#333",
    fontSize: "20px",
  },
  pre: {
    backgroundColor: "#f1f1f1",
    padding: "15px",
    borderRadius: "4px",
    overflowX: "auto",
    fontFamily: "Courier New, monospace",
    whiteSpace: "pre-wrap",
    wordBreak: "break-word",
    marginBottom: "15px",
  },
  mediaLinks: {
    marginTop: "20px",
    fontSize: "16px",
  },
  linkList: {
    listStyleType: "none",
    padding: 0,
  },
  linkItem: {
    marginBottom: "10px",
  },
  link: {
    color: "#007bff",
    textDecoration: "none",
  },
  linkHover: {
    textDecoration: "underline",
  },
};

export default Result;
