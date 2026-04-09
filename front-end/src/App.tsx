import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from "./pages/Home"
import ChatBot from "./components/ChatBot"
import Navbar from "./components/NavBar"
import ProviderList from "./components/ProviderList"

function App() {

  return (
      <BrowserRouter>
        <Navbar></Navbar>
        <Routes>
          <Route path="/" element={<Home></Home>}/>
          <Route path="/Home" element={<Home></Home>}/>
          <Route path="/ProviderList" element={<ProviderList></ProviderList>}/>
          <Route path="/ChatBot" element={<ChatBot></ChatBot>}/>
          </Routes>
      </BrowserRouter>
  )
}

export default App

