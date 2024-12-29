import "./style/signalHeader.css"

const SignalHeader = ({signal, additionalInfo = null}) => {

    const formatSignal = (signal) => {
        signal = signal.toLowerCase().replace("neutral", "Hold").replace("negative", "Sell").replace("positive", "Buy")
        return signal.charAt(0).toUpperCase() + signal.slice(1).toLowerCase();
    }

    const getSignalColor = (signal) => {
        if (typeof signal === 'string') {
            switch (signal.toLowerCase()) {
                case 'buy':
                case 'positive':
                    return 'bg-green-50 border-green-200 text-green-700';
                case 'sell':
                case 'negative':
                    return 'bg-red-50 border-red-200 text-red-700';
                default:
                    return 'bg-blue-50 border-blue-200 text-blue-700';
            }
        }
        return 'bg-blue-50 border-blue-200 text-blue-700';
    };

    return (
        <div className="signal-header">
            <div className="analysis-type">Analysis signal</div>
            <div className={`signal-container ${getSignalColor(signal)}`}>
                <span className="signal-value">{formatSignal(signal)}</span>
            </div>
            {additionalInfo && (
                <div className="signal-info">{additionalInfo}</div>
            )}
        </div>
    );
};

export default SignalHeader;