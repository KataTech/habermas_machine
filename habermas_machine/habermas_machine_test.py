# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from absl.testing import absltest
from absl.testing import parameterized

import habermas_machine as hm
import types
from social_choice import utils as sc_utils


class HabermasMachineTest(parameterized.TestCase):

  def test_habermas_machine(self):
    """Tests the habermas machine."""
    num_citizens = 2
    num_candidates = 3  # Generate only one candidate for easier checking
    question = 'What is the meaning of life?'
    opinions = ['42', 'To be happy.']
    critiques = ['I disagree.', 'I agree.']
    machine = hm.HabermasMachine(
        question=question,
        statement_client=types.LLMCLient.MOCK.get_client('mock_url'),
        reward_client=types.LLMCLient.MOCK.get_client('mock_url'),
        statement_model=types.StatementModel.MOCK.get_model(),
        reward_model=types.RewardModel.MOCK.get_model(),
        social_choice_method=types.RankAggregation.SCHULZE.get_method(
            tie_breaking_method=sc_utils.TieBreakingMethod.TIES_ALLOWED
        ),
        num_candidates=num_candidates,
        num_citizens=num_citizens,
        seed=0,
    )

    # Test initial state.
    self.assertEqual(machine._round, 0)
    self.assertEmpty(machine._opinions)
    self.assertEmpty(machine._critiques)
    self.assertEmpty(machine._previous_winners)
    self.assertEmpty(machine._previous_candidates)
    self.assertEqual(machine._num_citizens, num_citizens)
    self.assertEqual(machine._num_candidates, num_candidates)
    self.assertEqual(machine._verbose, False)
    self.assertEqual(machine._question, question)

    # Test overwrite previous winner.
    with self.assertRaises(ValueError):
      machine.overwrite_previous_winner('winner1')

    # Test opinion round.
    winner, sorted_statements = machine.mediate(opinions)

    self.assertEqual(machine._round, 1)
    self.assertEqual(machine._question, question)
    self.assertSequenceEqual(machine._opinions, opinions)
    self.assertEmpty(machine._critiques)
    self.assertSequenceEqual(machine._previous_winners, [winner])
    self.assertSequenceEqual(machine._previous_candidates, [sorted_statements])
    self.assertIn(winner, sorted_statements)
    for statement in sorted_statements:
      self.assertIn(question, statement)
      for opinion in opinions:
        self.assertIn(opinion, statement)

    # Test critique round.
    winner2, sorted_statements2 = machine.mediate(critiques)

    self.assertEqual(machine._round, 2)
    self.assertEqual(machine._question, question)
    self.assertSequenceEqual(machine._opinions, opinions)
    self.assertSequenceEqual(machine._critiques, [critiques])
    self.assertSequenceEqual(machine._previous_winners, [winner, winner2])
    self.assertSequenceEqual(
        machine._previous_candidates, [sorted_statements, sorted_statements2]
    )
    self.assertIn(winner2, sorted_statements2)
    for statement in sorted_statements2:
      self.assertIn(question, statement)
      for opinion in opinions:
        self.assertIn(opinion, statement)
      for critique in critiques:
        self.assertIn(critique, statement)

    # Test overwrite previous winner.
    machine.overwrite_previous_winner('winner3')
    self.assertEqual(machine._previous_winners[-1], 'winner3')

  def test_wrong_number_of_opinions(self):
    num_citizens = 2
    machine = hm.HabermasMachine(
        question='Question?',
        statement_client=types.LLMCLient.MOCK.get_client('mock_url'),
        reward_client=types.LLMCLient.MOCK.get_client('mock_url'),
        statement_model=types.StatementModel.MOCK.get_model(),
        reward_model=types.RewardModel.MOCK.get_model(),
        social_choice_method=types.RankAggregation.SCHULZE.get_method(
            tie_breaking_method=sc_utils.TieBreakingMethod.TIES_ALLOWED
        ),
        num_citizens=num_citizens,
        seed=0,
    )
    with self.assertRaises(ValueError):
      _, _ = machine.mediate(['opinion1'])

  def test_wrong_number_of_critiques(self):
    num_citizens = 2
    machine = hm.HabermasMachine(
        question='Question?',
        statement_client=types.LLMCLient.MOCK.get_client('mock_url'),
        reward_client=types.LLMCLient.MOCK.get_client('mock_url'),
        statement_model=types.StatementModel.MOCK.get_model(),
        reward_model=types.RewardModel.MOCK.get_model(),
        social_choice_method=types.RankAggregation.SCHULZE.get_method(
            tie_breaking_method=sc_utils.TieBreakingMethod.TIES_ALLOWED
        ),
        num_citizens=num_citizens,
        seed=0,
    )
    _, _ = machine.mediate(['opinion1', 'opinion2'])  # Opinion round.
    with self.assertRaises(ValueError):
      machine.mediate(['critique1', 'critique2', 'critique3'])


if __name__ == '__main__':
  absltest.main()
