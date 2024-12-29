import './style/contactDetails.css'
import Logo from "../images/Logo.png";

function ContactDetails() {
    return (
        <div className="ContactDetails">
            <div className="contact-details-container">
                <h2>Contact Details</h2>
                <div className="contact-item">
                    <h3>Email</h3>
                    <p>macedonianmarketpulse@gmail.com</p>
                </div>
                <div className="contact-item">
                    <h3>Address</h3>
                    <p>Partizanska br.163, 1000 Skopje Macedonia</p>
                </div>
                <div className="contact-item">
                    <h3>Phone Number</h3>
                    <p>+38970123456</p>
                </div>
                <div className="contact-item">
                    <img src={Logo} alt="Logo" className="logo-image" />
                </div>
            </div>
        </div>
    );
}

export default ContactDetails;