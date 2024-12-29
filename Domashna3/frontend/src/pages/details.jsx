import {useState, useEffect} from 'react';
import {useLocation} from 'react-router-dom';
import axios from 'axios';
import LoadingScreen from "../components/loadingScreen.jsx";
import StockPriceChart from "../components/graph.jsx";
import StockAnalysis from "../components/analysis-components/stockAnalysis.jsx";
import "./style/details.css"

const backendUrl = import.meta.env.VITE_BACKEND_URL || "http://localhost:8080";

const DetailsPage = () => {
    const location = useLocation();
    const issuer = location.state?.issuer;

    const [issuerData, setIssuerData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchIssuerData = async () => {
            if (!issuer) {
                setError('No issuer selected');
                setLoading(false);
                return;
            }
            try {
                setLoading(true);
                const response = await axios.get(`${backendUrl}/api/issuer-data/${issuer}`);
                setIssuerData(response.data);
                setError(null);
            } catch (err) {
                console.error('Error fetching issuer data:', err);
                setError(err.response ? `Error: ${err.response.status} - ${err.response.statusText}` : 'Network error occurred');
            } finally {
                setLoading(false);
            }
        };

        fetchIssuerData();
    }, [issuer]);

    const renderTable = () => {
        if (!issuerData) return null;

        const sortedData = Object.values(issuerData).sort((a, b) => {
            const dateA = new Date(a.date);
            const dateB = new Date(b.date);
            return dateB - dateA;
        });

        return (
            <div className="table-wrapper">
                <table>
                    <thead>
                    <tr>
                        <th>Date</th>
                        <th>Last trade price</th>
                        <th>Maximum</th>
                        <th>Minimum</th>
                        <th>Average Price</th>
                        <th>% Change</th>
                        <th>Volume</th>
                        <th>Turnover in BEST</th>
                        <th>Total turnover</th>
                    </tr>
                    </thead>
                    <tbody>
                    {sortedData.map((row, idx) => (
                        <tr key={idx}>
                            {Object.values(row).slice(1).map((val, index) => (
                                <td key={index}>
                                    {index === 0
                                        ? new Date(val).toLocaleDateString('en-GB', {
                                            day: '2-digit',
                                            month: '2-digit',
                                            year: 'numeric',
                                        }).replace(/\//g, '.')
                                        : val
                                    }
                                </td>
                            ))}
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        );
    };

    return (
        <div className="details-page">
            <h1 className="page-title">Issuer Details: {issuer}</h1>

            {loading && (
                <div className="loading-container">
                    <LoadingScreen />
                </div>
            )}

            {error && (
                <div className="error-container">
                    <p>{error}</p>
                </div>
            )}

            {!loading && issuerData && (
                <div className="chart-container">
                    <StockPriceChart issuerData={issuerData} />
                </div>
            )}

            {!loading && !error && issuerData && renderTable()}

            {!loading && !error && !issuerData && (
                <p className="no-data">No data available for this issuer.</p>
            )}

            <hr className="divider" />

            <div className="analysis-container">
                <StockAnalysis issuer={issuer} />
            </div>
        </div>
    );
};

export default DetailsPage;
