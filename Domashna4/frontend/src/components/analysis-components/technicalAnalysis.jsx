import {useState} from 'react';
import "./style/technicalAnalysis.css"
import SignalHeader from "./signalHeader.jsx";

const TechnicalAnalysis = ({data}) => {
    const [timeframe, setTimeframe] = useState('daily');

    const calculateOverallSignal = (signals) => {
        let buyCount = 0, sellCount = 0, holdCount = 0;
        Object.values(signals).forEach(signal => {
            if (signal === 'Buy') buyCount++;
            else if (signal === 'Sell') sellCount++;
            else holdCount++;
        });
        if (buyCount > sellCount && buyCount > holdCount) return 'Buy';
        if (sellCount > buyCount && sellCount > holdCount) return 'Sell';
        return 'Hold';

    };

    const timeframeData = data[timeframe];

    const movingAverages = {
        SMA_20_Signal: timeframeData.SMA_20_Signal,
        EMA_20_Signal: timeframeData.EMA_20_Signal,
        WMA_20_Signal: timeframeData.WMA_20_Signal,
        TRIX_Signal: timeframeData.TRIX_Signal,
        MACD_Signal: timeframeData.MACD_Signal,
    };

    const oscillators = {
        PPO_Signal: timeframeData.PPO_Signal,
        RSI_Signal: timeframeData.RSI_Signal,
        'Stoch_%K_Signal': timeframeData['Stoch_%K_Signal'],
        Williams_R_Signal: timeframeData.Williams_R_Signal,
        ROC_Signal: timeframeData.ROC_Signal,
        CCI_Signal: timeframeData.CCI_Signal,
    };


    const renderTable = (signals) => (
        <table className="analysis-table">
            <thead>
            <tr>
                <th>Indicator</th>
                <th>Signal</th>
            </tr>
            </thead>
            <tbody>
            {Object.entries(signals).map(([indicator, signal]) => (
                <tr key={indicator}>
                    <td>{indicator.replace('_Signal', '').replace("_", " ")}</td>
                    <td className={`signal ${signal.toLowerCase()}`}>{signal}</td>
                </tr>
            ))}
            </tbody>
        </table>
    );

    const overallSignal = calculateOverallSignal(timeframeData);

    return (
        <div className="technical-analysis">
            <h2 className="title">Technical Analysis</h2>

            <SignalHeader
                signal={overallSignal}
                // type={"technical analysis"}
            />

            <div className="timeframe-buttons">
                {['daily', 'weekly', 'monthly'].map(tf => (
                    <button
                        key={tf}
                        className={`timeframe-button ${timeframe === tf ? 'active' : ''}`}
                        onClick={() => setTimeframe(tf)}
                    >
                        {tf.charAt(0).toUpperCase() + tf.slice(1)}
                    </button>
                ))}
            </div>

            <div className="tables-container">
                <div className="table-section">
                    <h3>Moving Averages</h3>
                    {renderTable(movingAverages)}
                </div>

                <div className="table-section">
                    <h3>Oscillators</h3>
                    {renderTable(oscillators)}
                </div>
            </div>
        </div>
    );
};

export default TechnicalAnalysis;