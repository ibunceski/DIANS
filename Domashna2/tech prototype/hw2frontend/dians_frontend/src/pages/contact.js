import ContactForm from "../components/contactForm";
import ContactDetails from "../components/contactDetails";
import './style/contact.css'

function Contact() {
    return (
        <div className="Contact">
            <div className="contact-heading"><h1 className="contact-heading">CONTACT US</h1></div>
            <div className="form-details">
                <div className="contact-form-container">
                    <ContactForm />
                </div>
                <div className="contact-detail-container">
                    <ContactDetails />
                </div>
            </div>
        </div>
    );
}

export default Contact;