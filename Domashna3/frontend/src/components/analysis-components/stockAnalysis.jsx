import "../style/stockAnalysis.css";
import {useState, useEffect} from "react";
import axios from "axios";
import TechnicalAnalysis from "./technicalAnalysis.jsx";
import LSTMAnalysis from "./lstmAnalysis.jsx";
import FundamentalAnalysis from "./fundamentalAnalysis.jsx";
import LoadingScreen from "../loadingScreen.jsx";

const backendUrl = import.meta.env.VITE_BACKEND_URL || "http://localhost:8080";

const StockAnalysis = ({issuer}) => {
    const [selectedAnalysis, setSelectedAnalysis] = useState("Technical Analysis");
    const [analysisData, setAnalysisData] = useState({
        technical: null,
        fundamental: null,
        lstm: null,
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchAllData = async () => {
            try {
                const [technicalResponse, fundamentalResponse, lstmResponse] = await Promise.all([
                    axios.get(`${backendUrl}/api/technical/${issuer}`),
                    axios.get(`${backendUrl}/api/nlp/${issuer}`),
                    axios.get(`${backendUrl}/api/lstm/${issuer}`),
                ]);

                setAnalysisData({
                    technical: technicalResponse.data,
                    fundamental: fundamentalResponse.data,
                    lstm: lstmResponse.data,
                });
            } catch (err) {
                setError("Failed to fetch analysis data");
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchAllData();
    }, [issuer]);


    if (loading) return <div><h1>Analysis</h1><LoadingScreen/></div>;
    if (error) return <p>{error}</p>;

    const renderContent = () => {
        switch (selectedAnalysis) {
            case "Technical Analysis":
                return <TechnicalAnalysis data={analysisData.technical}
                />;
            case "Fundamental Analysis":
                return <FundamentalAnalysis data={analysisData.fundamental}
                />;
            case "LSTM Stock Price Prediction":
                return <LSTMAnalysis data={analysisData.lstm}/>;
            default:
                return <p>Select an analysis to view details.</p>;
        }
    };

    return (
        <div>
            <h1>Analysis</h1>
            {/*<div className='analysis-summary'>*/}
            {/*    {Object.values(analysisSignal).every(value => value !== null) && (*/}
            {/*        Object.entries(analysisSignal).map(([key, value]) => (*/}
            {/*            <p key={key}>{key + ':' + value}</p>*/}
            {/*        ))*/}
            {/*    )}*/}
            {/*</div>*/}
            <div className="analysis-grid">
                <div
                    className="analysis-box"
                    onClick={() => setSelectedAnalysis("Technical Analysis")}
                >
                    Technical Analysis
                </div>
                <div
                    className="analysis-box"
                    onClick={() => setSelectedAnalysis("Fundamental Analysis")}
                >
                    Fundamental Analysis
                </div>
                <div
                    className="analysis-box"
                    onClick={() => setSelectedAnalysis("LSTM Stock Price Prediction")}
                >
                    LSTM Stock Price Prediction
                </div>
            </div>

            <div className="analysis-content">{renderContent()}</div>
        </div>
    );
};

export default StockAnalysis;