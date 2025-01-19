import {useState, useEffect} from 'react';
import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend} from 'recharts';
import "./style/lstmAnalysis.css"
import SignalHeader from "./signalHeader.jsx";

const LSTMAnalysis = ({data}) => {
    const [graphData, setGraphData] = useState([]);
    const [yAxisDomain, setYAxisDomain] = useState([0, 0]);
    const [dailyPercent, setDailyPercent] = useState([]);
    const [signal, setSignal] = useState([]);

    useEffect(() => {
        if (!data) return;


        const actualData = data.recentDates.map((date, index) => ({
            date: new Date(date),
            actual: data.actualPrices[index],
            predicted: null,
        }));

        const predictedData = data.dates.map((date, index) => ({
            date: new Date(date),
            actual: null,
            predicted: Math.round(data.predictedPrices[index]),
        }));

        const combinedData = [...actualData, ...predictedData];
        setGraphData(combinedData);
        setDailyPercent(data.dailyPercent);
        setSignal(data.signal);

        const prices = combinedData
            .map((item) => item.actual || item.predicted)
            .filter((price) => price != null);
        const minPrice = Math.floor(Math.min(...prices));
        const maxPrice = Math.floor(Math.max(...prices));

        const roundedMin = Math.round((minPrice * 0.98) / 100) * 100;
        const roundedMax = Math.round((maxPrice * 1.02) / 100) * 100;

        setYAxisDomain([roundedMin, roundedMax]);
    }, [data]);


    const CustomTooltip = ({active, payload, label}) => {
        if (active && payload && payload.length) {
            return (
                <div className="custom-tooltip">
                    <p className="tooltip-date">{new Date(label).toLocaleDateString()}</p>
                    {payload.map((item, index) => (
                        item.value && (
                            <p key={index} className="tooltip-value" style={{color: item.color}}>
                                {item.name}: {item.value.toLocaleString()}
                            </p>
                        )
                    ))}
                </div>
            );
        }
        return null;
    };

    if (!graphData.length) {
        return <div className="loading">There is not enough data for the LSTM Analysis to be done</div>;
    }

    return (
        <div className="lstm-analysis">
            <h2 className="title">LSTM Analysis</h2>
            <SignalHeader
                signal={signal}
                // type={"LSTM analysis"}
                // additionalInfo={dailyPercent.join(' | ')}
            />
            <div className="chart-container">
                <LineChart
                    width={800}
                    height={400}
                    data={graphData}
                    margin={{top: 5, right: 30, left: 20, bottom: 5}}
                >
                    <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0"/>
                    <XAxis
                        dataKey="date"
                        tickFormatter={(str) => new Date(str).toLocaleDateString()}
                        tick={{fontSize: 12, fill: '#2c3e50'}}
                        stroke="#8884d8"
                    />
                    <YAxis
                        domain={yAxisDomain}
                        tick={{fontSize: 12, fill: '#2c3e50'}}
                        stroke="#8884d8"
                    />
                    <Tooltip content={<CustomTooltip/>}/>
                    <Legend
                        wrapperStyle={{
                            paddingTop: '20px',
                            fontSize: '14px'
                        }}
                    />
                    <Line
                        type="monotone"
                        dataKey="actual"
                        stroke="#3f51b5"
                        strokeWidth={2}
                        dot={false}
                        name="Actual Prices"
                        activeDot={{r: 6}}
                    />
                    <Line
                        type="monotone"
                        dataKey="predicted"
                        stroke="#00c853"
                        strokeWidth={2}
                        dot={false}
                        name="Predicted Prices"
                        activeDot={{r: 6}}
                    />
                </LineChart>
            </div>

            <div className="daily-percent">
                {dailyPercent.map((day, index) => (
                    <p key={day + index}>{day}</p>
                ))}
            </div>
        </div>
    );
};

export default LSTMAnalysis;