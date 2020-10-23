# Conversational Semantic Parsing for Dialog State Tracking

We introduce TreeDST (**T**ree-based **D**ialog **S**tate **T**racking), a multi-turn, multi-domain task-oriented dialog dataset annotated with tree-based user dialog states and system dialog acts. The goal of this dataset is to provide a novel solution for end-to-end dialog state tracking as a conversational semantic parsing task. Please refer to our paper for [Conversational Semantic Parsing for Dialog State Tracking](https://arxiv.org/pdf/2010.12770.pdf) for details.

## Task Description

The task in TreeDST is to predict the user dialog state for each turn of a conversation. The dialog state is a representation of the user's goal up to the current turn of the conversation.

## Dataset Description

The dataset contains 27,280 conversations covering 10 domains with shared types of person, time and location. The dataset and schema can be accessed in the [dataset](dataset) folder. A tool for visualizing the data is in the "dotted" format is provided at [utils](utils) folder.


## License

The code in this repository is licensed according to the [LICENSE](LICENSE) file.

The TreeDST dataset is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/.

## Declaration

This dataset contains computer-generated synthetic conversation flows that has been human annotated to provide richer and more natural dialogue. **This dataset does not include any data from Siri production users**.
