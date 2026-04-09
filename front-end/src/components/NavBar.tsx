import { Link } from "react-router-dom"
import "../css/NavBar.css"

function Navbar() {
    return(
        <>
        <h2>Navbar</h2>
        <Link to="/"></Link>
        <Link to="/Home">Home</Link>
        <Link to="/ProviderList">ProviderList</Link>
        <Link to="/ChatBot">ChatBot</Link>
        </>
    )
}

export default Navbar

