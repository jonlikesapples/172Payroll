import React, { Component } from 'react';
import axios from 'axios';
import {Redirect} from "react-router-dom";
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
  
const greeting = {margin:'2.5rem auto', textAlign:'center'}

class Login extends Component {
    constructor(props) {
		super(props)
		this.state = {
            email:'',
            password:'',
            code:null,
            message:"",
            token:'',
            redirect:false
        }
        //this.Auth = new Authserver();
        this.handleFormSubmit = this.handleFormSubmit.bind(this)
	}

    
    ////////////////Login ////////////////////
    onChange = ({ target: { name, value } }) => {
        this.setState({ [name]: value })
    }

    handleFormSubmit = (e) =>{
        e.preventDefault();
        const user = {
            email : this.state.email,
            password : this.state.password
        }
        axios.post('/api/login',{user})
            .then(res =>{
                console.log(res.data)
                if(res.data.http_code === 200)
                {
                    const id_token = res.data.userID
                    localStorage.setItem('id_token',id_token)
                    localStorage.setItem('admin',res.data.admin)
                    this.setState({redirect:true,admin:res.data.admin, info:res.data.value})
                }
            })
    }

    updateForm = (newState) =>{
        this.setState({
            State:newState
        })
    }
    

render(){
    const {redirect,admin,info} = this.state

    if (redirect && admin === 1) {
        return (
          <Redirect
            to={{
              pathname: "/employeesTable",
              state : {info:info}
            }}
          />
        );
      } else if(redirect){
          return(
        <Redirect
        to={{
          pathname: "/employee",
          state : {info:info}
        }}
      />
          )
      }

    return (   
        <div style={{
            height: window.innerHeight+'px',
            overflow: 'auto',
            display: 'flex',
            alignItems: 'center',
            backgroundColor:"#ececec"
          }} > 
        <div style={{
            margin: 'auto',
            backgroundColor: 'white',
            borderRadius: '10px',
            maxWidth: `${0.5*window.innerWidth}px`,
            minWidth: '250px',
            textAlign:"center",
            border:"2px solid #c2c2c2"
          }} >
              <div style={greeting}>
                  <h2 style={{margin:'1rem 2rem',borderBottom:"1px solid red"}}>A Company</h2>
                  <h5>Log in with your email address and password</h5>
              </div>
            <form
              onSubmit={this.handleFormSubmit}
              formProps={{}}
            >
              <input
                placeholder="Email"
                name="email"
                type="email"
                onChange={this.onChange}
                validations={{isEmail: null, isLength: {min: 3, max: 30}}}
                validationErrorText="Sorry, please enter a valid email."
                required
              /><br/>
              <input
                placeholder="Password"
                name="password"
                type="password"
                onChange={this.onChange}
                hintText="min. 8 characters"
                validations={{isLength: {min: 8, max: 64}}}
                validationErrorText="Sorry, password must be min. 8 characters."
                required
              />
              <button className="btn btn-info" type="submit" style={{margin: '6% 15% 3% 15%', width: '70%', height:'2.2em'}} >
                Log In
              </button>
            </form>
          </div>
          </div>
    );
}   
};

Login.propTypes = {
    classes: PropTypes.object.isRequired,
  };
  
  export default withStyles(styles)(Login);