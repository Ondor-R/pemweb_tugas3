import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [productName, setProductName] = useState('');
  const [reviewText, setReviewText] = useState('');
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(false);

  // Fetch reviews saat aplikasi dibuka
  useEffect(() => {
    fetchReviews();
  }, []);

  const fetchReviews = async () => {
    try {
      const res = await fetch('http://localhost:6543/api/reviews');
      const data = await res.json();
      setReviews(data);
    } catch (error) {
      console.error("Error fetching reviews:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch('http://localhost:6543/api/analyze-review', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_name: productName, review_text: reviewText }),
      });
      
      if (response.ok) {
        await fetchReviews();
        setProductName('');
        setReviewText('');
      } else {
        alert("Gagal menganalisa review");
      }
    } catch (error) {
      alert("Error koneksi ke server");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Product Review Analyzer</h1>
      
      {/* Form Input */}
      <div className="form-card">
        <h3>New Review</h3>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <input 
              type="text" 
              className="form-input"
              placeholder="Product Name" 
              value={productName}
              onChange={(e) => setProductName(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <textarea 
              className="form-textarea"
              placeholder="Write your review here..." 
              value={reviewText}
              onChange={(e) => setReviewText(e.target.value)}
              required
              rows="4"
            />
          </div>
          <button type="submit" disabled={loading} className="btn-submit">
            {loading ? 'Analyzing with AI...' : 'Submit Analysis'}
          </button>
        </form>
      </div>

      {/* Results Display */}
      <h3>Analysis Results</h3>
      <div className="review-list">
        {reviews.map((review) => (
          <div key={review.id} className="review-card">
            <h4>{review.product_name}</h4>
            <p className="review-text">"{review.review_text}"</p>
            <hr />
            <p>
              <strong>Sentiment: </strong> 
              <span className={`sentiment-label ${review.sentiment === 'POSITIVE' ? 'sentiment-positive' : 'sentiment-negative'}`}>
                 {review.sentiment}
              </span>
            </p>
            <div>
              <strong>Key Points (Gemini):</strong>
              <ul className="key-points-list">
                {review.key_points.map((point, idx) => (
                  <li key={idx}>{point}</li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;