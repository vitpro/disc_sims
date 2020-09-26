import React, { Component } from 'react';
import Tabs from './Tabs';

export default class RacePicker extends Component {

    render() {
        return (
            <div className="racePickerGrid">
               <Tabs>
                   <div label="Horde">
                       horde icons :)
                   </div>
                   <div label="Alliance">
                       alliance icons!
                   </div>
               </Tabs>
            </div>
        );
    }
}