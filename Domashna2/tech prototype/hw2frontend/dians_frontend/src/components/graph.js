import "./style/graph.css"
import React from 'react';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer
} from 'recharts';

const StockPriceChart = ({issuerData}) => {
    const maxDots = 40;
    const totalDataPoints = Object.values(issuerData).length;
    const step = Math.max(Math.floor(totalDataPoints / maxDots), 1);

    const chartData = Object.values(issuerData)
        .filter((_, index) => index % step === 0)
        .map(row => ({
            date: row['date'],
            lastPrice: row['lastTradePrice'].replace('.', '').replace(',', '.')
        }));


    const prices = chartData.map(row => row.lastPrice);
    const minPrice = Math.min(...prices);
    const maxPrice = Math.max(...prices);
    const priceRange = maxPrice - minPrice;
    const yAxisDomain = [minPrice - priceRange * 0.1, maxPrice + priceRange * 0.1];

    return (
        <div className="chart-container">
            <ResponsiveContainer width="100%" height={400}>
                <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3"/>
                    <XAxis
                        dataKey="date"
                        domain={['auto', 'auto']}
                        tick={{fontSize: 10}}
                    />
                    <YAxis
                        domain={yAxisDomain}
                        tickCount={6}
                        tick={{fontSize: 10}}
                        tickFormatter={(value) => Math.round(value)}
                    />
                    <Tooltip/>
                    <Legend/>
                    <Line
                        type="linear"
                        dataKey="lastPrice"
                        stroke="#8884d8"
                        activeDot={{r: 8}}
                        name="Last Trade Price"
                        dot={true}
                        animationDuration={1000}
                        animationEasing='ease-in-out'
                        isAnimationActive={true}
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default StockPriceChart;
