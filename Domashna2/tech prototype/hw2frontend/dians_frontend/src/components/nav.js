import './style/nav.css'
import { FiHome } from "react-icons/fi";
import { IoPersonOutline } from "react-icons/io5";
import { LiaPhoneSquareSolid } from "react-icons/lia";

function nav() {
    return (
        <div className="Nav">
            <header className="header">

                <nav className="header-nav">
                    <ul className="header-links">
                        <li className="header-link left">
                            <a href="/" className="link-container">
                                <FiHome size={40}/>
                                <span>Home</span>
                            </a>
                        </li>
                        <li className="header-link center">
                            <a href="/about" className="link-container">
                                <IoPersonOutline size={40}/>
                                <span>About Us</span>
                            </a>
                        </li>
                        <li className="header-link right">
                            <a href="/contact" className="link-container">
                                <LiaPhoneSquareSolid size={40}/>
                                <span>Contact Us</span>
                            </a>
                        </li>
                    </ul>
                </nav>
            </header>
        </div>
    );
}

export default nav;