import React, {useState, useEffect} from 'react';
import {useLocation} from 'react-router-dom';
import axios from 'axios';
import LoadingScreen from "../components/loadingScreen";
import StockPriceChart from "../components/graph";
import './style/details.css';

const DetailsPage = () => {
    const location = useLocation();
    const issuer = location.state?.issuer;

    const [issuerData, setIssuerData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const checkAndPerformScraping = async () => {
            const lastScrapedDate = localStorage.getItem('lastScrapedDate');
            const today = new Date().toISOString().split('T')[0];

            if (!lastScrapedDate || lastScrapedDate !== today) {
                try {
                    setLoading(true)
                    await axios.get('http://localhost:8080/api/fill-data');
                    localStorage.setItem('lastScrapedDate', today);
                } catch (err) {
                    console.error('Scraping error:', err);
                }
            }
        };

        const fetchIssuerData = async () => {
            if (!issuer) {
                setError('No issuer selected');
                setLoading(false);
                return;
            }

            try {
                setLoading(true);
                const response = await axios.get(`http://localhost:8080/api/issuer-data/${issuer}`);
                setIssuerData(response.data);
                setError(null);
            } catch (err) {
                console.error('Error fetching issuer data:', err);
                setError(err.response ? `Error: ${err.response.status} - ${err.response.statusText}` : 'Network error occurred');
            } finally {
                setLoading(false);
            }
        };

        const initializePage = async () => {
            await checkAndPerformScraping();
            await fetchIssuerData();
        };

        initializePage();
    }, [issuer]);

    const renderTable = () => {
        if (!issuerData) return null;
        return (
            <div className='table-container'>
                <table>
                    <thead>
                    <th>Датум</th>
                    <th>Цена на последна трансакција</th>
                    <th>Максимум</th>
                    <th>Минимум</th>
                    <th>Просечна цена</th>
                    <th>%пром.</th>
                    <th>Количина</th>
                    <th>Промет во БЕСТ во денари</th>
                    <th>Вкупен промет во денари</th>
                    </thead>
                    <tbody>{Object.values(issuerData).map(row => {
                        return <tr>{Object.values(row).slice(1).map(val => {
                            return <td>{val}</td>
                        })}</tr>
                    })}
                    </tbody>
                </table>
            </div>
        );
    };

    return (
        <div>
            <h1>Issuer Details: {issuer}</h1>

            {loading && <LoadingScreen/>}

            {error && (
                <div>
                    <p>{error}</p>
                </div>
            )}

            {!loading && issuerData && (
                <div className="chart-container">
                    <StockPriceChart issuerData={issuerData}/>
                </div>
            )}

            {!loading && !error && issuerData && renderTable()}

            {!loading && !error && !issuerData && (
                <p>No data available for this issuer.</p>
            )}

            <div className="analysis-grid">
                <div className="analysis-box">Technical Analysis</div>
                <div className="analysis-box">Fundamental Analysis</div>
                <div className="analysis-box">LSTM Stock Price Prediction</div>
            </div>
        </div>
    );
};

export default DetailsPage;
