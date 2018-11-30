import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom';

import '../node_modules/bootstrap/dist/css/bootstrap.min.css'

import Routes from './route'

class App extends Component {
    render() {
      return (
        <BrowserRouter>
            <Routes/>
        </BrowserRouter>
      );
    }
  }

ReactDOM.render(<App />, document.getElementById('root'));

