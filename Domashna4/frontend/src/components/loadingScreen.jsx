import {Bars} from 'react-loader-spinner';
import "./style/loadingScreen.css"

const LoadingScreen = () => {

    return (
        <div className="loading--screen">
            <Bars
                color="#4267B2"
                height={100}
                width={100}
            />
            <br/>
            <p className="message">Please wait while we are preparing the stock data</p>
        </div>

    )
}

export default LoadingScreen;