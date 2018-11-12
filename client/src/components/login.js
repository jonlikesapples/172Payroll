import React, { Component } from 'react';

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
    }

    updateForm = (newState) =>{
        this.setState({
            State:newState
        })
    }
    

render(){
    return (
        <div className="login_container" style ={{marginLeft:"25%",marginRight:'25%',alignItems: 'center',border:"1px solid #c2c2c2"}}>
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
    );
}   
};

export default Login;