import React, {useEffect, useState} from 'react';
import axios from 'axios';
import Logo from '../images/Logo.png';
import SearchBar from '../components/search';
import './style/home.css';
import LoadingScreen from "../components/loadingScreen";

function Home() {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);


    useEffect(() => {
        const checkAndPerformScraping = async () => {
            const lastScrapedDate = localStorage.getItem('lastScrapedDate');
            const today = new Date().toISOString().split('T')[0];

            if (!lastScrapedDate || lastScrapedDate !== today) {
                try {
                    setLoading(true)
                    setError(null);
                    await axios.get('http://localhost:8080/api/fill-data');

                    localStorage.setItem('lastScrapedDate', today);
                } catch (err) {
                    setError(err.response ? `Error: ${err.response.status} - ${err.response.statusText}` : 'Network error occurred');
                } finally {
                    setLoading(false);
                }
            }else{
                setLoading(false)
            }
        };

        const initializePage = async () => {
            await checkAndPerformScraping();
        };

        initializePage();
    }, []);

    return (
        <div>

            {loading && <LoadingScreen/>}

            {error && (
                <div>
                    <p>{error}</p>
                </div>
            )}

            {!loading && <div className="Home">
                <img src={Logo} alt="Logo" className="logo"/>
                <SearchBar/>
            </div>}
        </div>);
}

export default Home;
