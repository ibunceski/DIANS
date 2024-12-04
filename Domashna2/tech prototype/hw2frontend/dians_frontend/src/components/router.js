import Home from '../pages/home'
import About from "../pages/about";
import Contact from "../pages/contact";
import Header from '../static/header'
import Footer from '../static/footer'
import Details from "../pages/details";
import { BrowserRouter, Routes, Route } from 'react-router-dom';


function Router() {
    return (

        <div className="Router">
            <Header />
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Home/>} />
                    <Route path="/about" element={<About/>} />
                    <Route path="/contact" element={<Contact/>} />
                    <Route path="/details" element={<Details/>} />
                </Routes>
            </BrowserRouter>
            <Footer />

        </div>
    );
}

export default Router;