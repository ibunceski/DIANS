import Home from '../pages/home.jsx'
import About from "../pages/about.jsx";
import Contact from "../pages/contact.jsx";
import Header from '../static/header.jsx'
import Footer from '../static/footer.jsx'
import Details from "../pages/details.jsx";
import {BrowserRouter, Routes, Route} from 'react-router-dom';

function Router() {
    return (
        <div className="Router">
            <BrowserRouter>
                <Header/>
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/about" element={<About/>}/>
                    <Route path="/contact" element={<Contact/>}/>
                    <Route path="/details" element={<Details/>}/>
                </Routes>
                <Footer/>
            </BrowserRouter>
        </div>
    );
}

export default Router;