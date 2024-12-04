import Logo from '../images/Logo.png'
import SearchBar from '../components/search'
import './style/home.css';

function Home() {
    return (
        <div className="Home">
            <img src={Logo} alt="Logo" className="logo" />
            <SearchBar/>
        </div>
    );
}

export default Home;