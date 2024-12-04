import React from 'react';
import { Bars } from 'react-loader-spinner';
import "./style/loadingScreen.css"

const LoadingScreen = (props) => {

    return (
        <div className="loading--screen">
            <Bars
                color="#4267B2"
                height={100}
                width={100}
            />
        </div>
    )
}

export default LoadingScreen;