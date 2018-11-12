import React, { Component } from 'react';
import {Switch, Route} from 'react-router-dom'

//////////////////////
import Login from './components/login'
import Create from './components/create'

class Routes extends Component {
    render() {
        return (
            <Switch> 
                 <Route path="/" exact component={Login} />
                 <Route path="/create" exact component={Create} />
            </Switch>
        );
    }
}

export default Routes;