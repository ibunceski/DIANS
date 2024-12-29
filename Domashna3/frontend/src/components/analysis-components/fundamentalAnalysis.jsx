import {ArrowUp, ArrowDown, Minus} from 'lucide-react';
import SignalHeader from "./signalHeader.jsx";
import {useEffect, useState} from "react";
import "./style/fundamentalAnalysis.css"

const FundamentalAnalysis = ({data}) => {

    const [signal, setSignal] = useState(null);
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(false)

    useEffect(() => {
            if (data.error !== undefined) {
                setError(true);
                return;
            }

            const findMajorityElement = (array) => {
                const countMap = array.reduce((acc, label) => {
                    acc[label] = (acc[label] || 0) + 1;
                    return acc;
                }, {});

                let maxCount = 0;
                let majorityElements = [];

                for (const [label, count] of Object.entries(countMap)) {
                    if (count > maxCount) {
                        maxCount = count;
                        majorityElements = [label];
                    } else if (count === maxCount) {
                        majorityElements.push(label);
                    }
                }

                return majorityElements;
            };

            const labels = data.map((item) => {
                return item.signal.label
            })
            setSignal(findMajorityElement(labels).join("/"))
            setLoading(false)
        }, [data],
    )

    const getSentimentIcon = (label) => {
        switch (label) {
            case 'positive':
                return <ArrowUp className="w-4 h-4 text-green-600"/>;
            case 'negative':
                return <ArrowDown className="w-4 h-4 text-red-600"/>;
            default:
                return <Minus className="w-4 h-4 text-blue-600"/>;
        }
    };


    return (
        <div>
            {error && <div><p>No news in the past 20 days, fundamental analysis cannot be done.</p></div>}
            {!error &&
                !loading &&
                <div className="fundamental-analysis">
                    <h2 className="title">Fundamental Analysis</h2>
                    <SignalHeader
                        signal={signal}
                        // type={"Fundamental"}
                    />
                    <div className="news-container">
                        {data.map((item, index) => (
                            <div
                                key={index}
                                className='news-item'
                            >
                                <div
                                    className='sentiment-badge'
                                >
                                    {getSentimentIcon(item.signal.label)}
                                    {item.signal.label}
                                    <span className="sentiment-score">
                                ({(item.signal.score * 100).toFixed(1)}%)
                            </span>
                                </div>
                                <div className="news-text">
                                    {item.text}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            }
        </div>
    );
};

export default FundamentalAnalysis;