import React, { useState } from 'react';
import { FaRegTimesCircle } from "react-icons/fa";
import Logo from "../images/Logo.png"
import "./style/about.css"

function About() {
    const [selectedBox, setSelectedBox] = useState(null);

    const handleClick = (boxId, content) => {
        setSelectedBox({ boxId, content });
    };

    const closeModal = () => {
        setSelectedBox(null);
    };

    const [isClosing, setIsClosing] = React.useState(false);

    const handleClose = () => {
        setIsClosing(true);
        setTimeout(() => {
            setSelectedBox(null);
            setIsClosing(false);
        }, 600);
    };

    return (
        <div className="About">
            <div className="container">
                <h1>About MacedonianMarketPulse</h1>
                <p className="intro">
                    Welcome to MacedonianMarketPulse, your gateway to insightful analysis and informed decisions about
                    the Macedonian stock market. Our mission is to empower investors, analysts, and market enthusiasts
                    with accurate, up-to-date data and cutting-edge insights.
                </p>
                <div className="grid">
                    <div
                        className="box"
                        id="who-we-are"
                        onClick={() => handleClick('Who We Are', 'MacedonianMarketPulse is a dedicated platform developed with a passion for finance, technology, and innovation. Our team combines expertise in software engineering, data science, and financial analysis to create a seamless experience for understanding and navigating the Macedonian stock market.')}
                    >
                        Who We Are
                    </div>
                    <div
                        className="box"
                        id="what-we-do"
                        onClick={() => handleClick('What We Do', 'We specialize in:' +
                            '\n' +
                            'Data Scraping: Automatically collecting and updating comprehensive data for issuers listed on the Macedonian stock market.\n' +
                            '\n' +
                            'Machine Learning Analysis: Leveraging advanced machine learning models to provide predictive insights, helping you make better investment decisions.\n' +
                            '\n' +
                            'Natural Language Processing: Analyzing textual data to extract trends, sentiments, and other valuable information.')}
                    >
                        What We Do
                    </div>
                    <div className="logo-container">
                        <img src={Logo} alt="MacedonianMarketPulse Logo" className="logo" />
                    </div>
                    <div
                        className="box"
                        id="our-vision"
                        onClick={() =>
                            handleClick('Our Vision', 'At MacedonianMarketPulse, we aim to bridge the gap between raw data and actionable intelligence. By combining technology with deep market understanding, we strive to make the Macedonian stock market accessible and transparent to everyone.')
                        }
                    >
                        Our Vision
                    </div>
                    <div
                        className="box"
                        id="why-choose-us"
                        onClick={() =>
                            handleClick('Why Choose Us', 'Comprehensive Data: Stay informed with complete and regularly updated market data.\n' +
                                '\n' +
                                'Advanced Analytics: Benefit from state-of-the-art machine learning and NLP techniques.\n' +
                                '\n' +
                                'User-Focused Design: Enjoy an intuitive and user-friendly platform tailored to your needs.\n' +
                                '\n' +
                                'Thank you for choosing MacedonianMarketPulse. Together, let’s unlock the full potential of the Macedonian stock market! ')
                        }
                    >
                        Why Choose Us
                    </div>
                </div>
            </div>

            {selectedBox && (
                <div className="modal-overlay" onClick={handleClose}>
                    <div
                        className={`modal-card ${isClosing ? 'exit' : ''}`}
                        onClick={(e) => e.stopPropagation()}
                    >
                        <FaRegTimesCircle className="close-button" onClick={handleClose} />
                        <h2>{selectedBox.boxId}</h2>
                        <p>{selectedBox.content}</p>
                    </div>
                </div>
            )}

        </div>
    );
}

export default About;