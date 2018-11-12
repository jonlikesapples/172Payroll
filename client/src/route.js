import React, { Component } from 'react';
import Login from './components/login'
import {Switch, Route} from 'react-router-dom'

class Routes extends Component {
    render() {
        return (
            <Switch> 
                 <Route path="/" exact component={Login} />
            </Switch>
        );
    }
}

export default Routes;