import './App.css';
import FileUpload from './components/FileUpload';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src= "https://www.permanentstyle.com/wp-content/uploads/2021/04/hang-up-vintage-london-580x464.jpg" width ={450} alt="logo" />
        <h1 className = "title">Tag Scanner</h1>
        <div><FileUpload>Wow</FileUpload></div>
      </header>
    </div>
  );
}

export default App;
