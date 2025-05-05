import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './styles.css';

const App = () => {
    const [tilbud, setTilbud] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchTilbud = async () => {
            try {
                const response = await axios.get("http://localhost:5000/tilbud");
                if (response.data.tilbud) {
                    setTilbud(response.data.tilbud);
                } else {
                    setTilbud([]);
                }
            } catch (err) {
                setError("Kunne ikke hente tilbud");
            } finally {
                setLoading(false);
            }
        };

        fetchTilbud();
    }, []);

    return (
        <div className="container">
            <h1>🔥 Smirnoff Ice Tilbud 🔥</h1>
            {loading && <div className="loader"></div>}
            {error && <p className="text-red">{error}</p>}
            {tilbud.length > 0 ? (
                <div className="tilbud-container">
                    {tilbud.map((item, index) => (
                        <div key={index} className="tilbud-card">
                            <img src={item.image} alt={item.name} />
                            <h2>{item.name}</h2>
                            <p className="price">{item.price}</p>
                            <p className="store">🛒 {item.store}</p>
                        </div>
                    ))}
                </div>
            ) : (
                !loading && <p className="text-gray">Der er ingen Smirnoff Ice på tilbud lige nu. 😢</p>
            )}
        </div>
    );
};

export default App;