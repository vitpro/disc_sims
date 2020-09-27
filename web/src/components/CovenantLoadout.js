import React, { Component } from 'react';
import Tabs from "./Tabs";

export default class CovenantLoadout extends Component {

    constructor(props) {
        super(props);
        this.state = {
            hover: false
        }
    }

    render() {
        return (
            <div>
                <Tabs listId="covenant-tab-list">
                    <div label="Covenant">
                        covenant
                    </div>
                    <div label="Conduits">
                        Conduits
                    </div>
                </Tabs>
            </div>
        );
    }
}