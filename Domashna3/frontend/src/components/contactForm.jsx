
import './style/contactForm.css';

function ContactForm() {
    return (
        <div className="ContactForm">
            <form className="contact-form">
                <h2>Contact Us</h2>

                <input
                    type="text"
                    name="name"
                    placeholder="Your Name"
                    className="contact-input"
                    required
                />

                <input
                    type="email"
                    name="email"
                    placeholder="Your Email"
                    className="contact-input"
                    required
                />

                <input
                    type="phone"
                    name="phone"
                    placeholder="Your Phone"
                    className="contact-input"
                />

                <textarea
                    name="comment"
                    placeholder="Your Comment"
                    className="contact-input"
                    required
                ></textarea>

                <button type="button" className="submit-btn">Submit</button>
            </form>
        </div>
    );
}

export default ContactForm;
