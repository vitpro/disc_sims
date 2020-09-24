import React, { Component } from 'react';
import styled from 'styled-components';

export default class Header extends Component {
    render() {
        return (
            <div className="header">
                <div id="headerLogo">
                    img and name
                </div>
                <a href="#" className="headerLink">Link 1</a>
                <a href="#" className="headerLink">Link 2</a>
                <a href="#" className="headerLink" id="headerDonate">Donate</a>
            </div>
        );
    }
}