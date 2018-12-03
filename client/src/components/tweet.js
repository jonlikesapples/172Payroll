import React, { Component } from 'react';
import axios from 'axios'

class Tweet extends Component {
    constructor(){
        super()
        this.state = {
            text:''
        }
        this.handleOnClick = this.handleOnClick.bind(this)
    }


    onChange = ({ target: { name, value } }) => {
        this.setState({ [name]: value })
    }

    handleOnClick(){
        var text = this.state.text;
        axios.post('/api/twitter',{text})
        .then(res => {
            console.log(res.data)
            if(res.data === 200){
                this.setState({success:'successfully tweet it'})
            }else{
                this.setState({error:"not able to tweet it"})
            }
            })
    }
    render() {
        return (
            <div className="container" style={{ textAlign: "center" }}>
                {this.state.success ?
                    <div className="alert alert-success" role="alert">
                        {this.state.success}
                    </div>
                    : null}
                {this.state.error ?
                    <div className="alert alert-danger" role="alert">
                        {this.state.error}
                    </div>
                    :
                    null
                }
                <div>
                    Enter what you want to tweet:<br/>
                <textarea
                        type="text"
                        placeholder="..."
                        name='text'
                        value={this.state.text}
                        onChange={this.onChange}
                        style={{width:300,height:400}}
                    />
                </div>
                <button type="submit" className="btn btn-info btn-sm" onClick={()=>this.handleOnClick()}>Post</button>
            </div>
        );
    }
}

export default Tweet;