import React, { Component } from 'react';
import axios from 'axios';

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
    return (    
        <div>
        <div className="login_container" style ={{border:"1px solid #c2c2c2",width:"50%",margin:"auto"}}>
        <form onSubmit={this.submitLogin}>
            <h2>Log in here</h2>
            <div className="form_element">
                <input 
                    type="text"
                    placeholder="Enter your username"
                    value={this.state.username}
                    onChange={this.handleInputUsername}
                />
            </div>
            <div className="form_element">
                <input 
                    type="password"
                    placeholder="Enter your password"
                    value={this.state.password}
                    onChange={this.handleInputPassword}
                />
            </div>
            <button type="submit">Log in</button>
            </form>
            </div>
            </div>
    );
}   
};

export default Login;