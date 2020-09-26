import React, { Component } from 'react';
import talentData from '../data/talent-data.json';
import Talent from "./Talent";

const getNeighbouringIndexes = idx => {
    const row_id = Math.floor(idx / 3);
    const neighbours = [row_id * 3, row_id * 3 + 1, row_id * 3 + 2];
    const index = neighbours.indexOf(idx);
    if (index > -1) {
        neighbours.splice(index, 1);
    }
    return neighbours;
};

export default class TalentPicker extends Component {

    constructor(props) {
        super(props);
        this.state = {
            selected_talents: [
                false, false, false,
                false, false, false,
                false, false, false,
                false, false, false,
                false, false, false,
                false, false, false,
                false, false, false,
            ],
        }
    }

    talentClickHandler = idx => {
        const selected_talents = this.state.selected_talents.slice();
        // mark this talent as selected
        selected_talents[idx] = true;
        const neighbouringIndexes = getNeighbouringIndexes(idx);
        // flip neighbouring talents as unselected
        for (let i = 0; i < neighbouringIndexes.length; i++) {
            selected_talents[neighbouringIndexes[i]] = false;
        }

        this.setState({
            ...this.state,
            selected_talents: selected_talents,
        });

        this.props.updateTalentsHandler(selected_talents);
    };

    render() {
        const talents = talentData[this.props.spec];
        return (
            <div>
                <h2 className="midTitle"> Talent</h2>
                <div className="talentGrid">

                    {talents.map((talent, idx) => (
                        <Talent
                            name={talent.name}
                            url={talent.img}
                            index={idx}
                            key={talent.name + idx.toString()}
                            talentClickHandler={this.talentClickHandler}
                            selected={this.state.selected_talents[idx]}
                        />
                    ))}

                </div>
            </div>
        );
    }
}