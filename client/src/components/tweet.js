import React, { Component } from 'react';
import axios from 'axios'

class Tweet extends Component {
    constructor(){
        super()
        this.state = {
            text:''
        }
    }


    onChange = ({ target: { name, value } }) => {
        this.setState({ [name]: value })
    }

    handleOnClick(){
        var text = this.state.text;
        axios.post('/api/twitter',{text})
        .then(res => {
            console.log(res.data)
        })
    }
    render() {
        return (
            <div className="container" style={{textAlign:"center"}}>
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