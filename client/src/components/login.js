import React, { Component } from 'react';
import axios from 'axios';

import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';

const styles = theme => ({
    button: {
      margin: theme.spacing.unit,
    },
    input: {
      display: 'none',
    },
  });
  

class Login extends Component {
    constructor(props) {
		super(props)
		this.state = {
            username:'',
            password:'',
            isAuth:false,
            code:null,
            message:"",
            token:''
        }
        this.submitLogin = this.submitLogin.bind(this)
        //this.Auth = new Authserver();
	}

    
    ////////////////Login ////////////////////
    handleInputUsername = (event) => {
        this.setState({username:event.target.value})
    }
    handleInputPassword = (event) => {
        this.setState({password:event.target.value})
    }


    submitLogin = (e) =>{
        e.preventDefault();
        let username = this.state.username;
        let password = this.state.password
        axios.post(`/api/login?username=${username}&password=${password}`)
            .then(res=>{   
                console.log(res.data)
            })

    }

    updateForm = (newState) =>{
        this.setState({
            State:newState
        })
    }
    

render(){
    const { classes } = this.props;

    return (    
        <div className="login_container" style={{textAlign:"center"}}>
            <Button variant="contained" color="primary" className={classes.button}>
                Sign in with Slack
            </Button>
            </div>
    );
}   
};

Login.propTypes = {
    classes: PropTypes.object.isRequired,
  };
  
  export default withStyles(styles)(Login);