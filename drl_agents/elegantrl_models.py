# RL models from elegantrl
import torch
import numpy as np
from logbook import Logger
from train.config import Arguments
from train.run import train_and_evaluate, init_agent

from drl_agents.agents import AgentDDPG, AgentPPO, AgentSAC, AgentTD3, AgentA2C

MODELS = {"ddpg": AgentDDPG, "td3": AgentTD3, "sac": AgentSAC, "ppo": AgentPPO, "a2c": AgentA2C}
OFF_POLICY_MODELS = ["ddpg", "td3", "sac"]
ON_POLICY_MODELS = ["ppo", "a2c"]
"""MODEL_KWARGS = {x: config.__dict__[f"{x.upper()}_PARAMS"] for x in MODELS.keys()}

NOISE = {
    "normal": NormalActionNoise,
    "ornstein_uhlenbeck": OrnsteinUhlenbeckActionNoise,
}"""


class DRLAgent:
    """Provides implementations for DRL algorithms
    Attributes
    ----------
        env: gym environment class
            user-defined class
    Methods
    -------
        get_model()
            setup DRL algorithms
        train_model()
            train DRL algorithms in a train dataset
            and output the trained model
        DRL_prediction()
            make a prediction in a test dataset and get train_results
    """

    def __init__(self, env, price_array, tech_array, env_params, if_log):
        self.log = Logger(self.__class__.__name__)
        self.env = env
        self.price_array = price_array
        self.tech_array = tech_array
        self.env_params = env_params
        self.if_log = if_log

    def get_model(self, model_name, gpu_id, model_kwargs):

        env_config = {
            "price_array": self.price_array,
            "tech_array": self.tech_array,
            "if_train": False,
        }

        env = self.env(config=env_config,
                       env_params=self.env_params,
                       if_log=self.if_log)

        env.env_num = 1
        agent = MODELS[model_name]
        if model_name not in MODELS:
            raise NotImplementedError("NotImplementedError")

        model = Arguments(agent=agent, env=env)
        model.learner_gpus = gpu_id

        if model_name in OFF_POLICY_MODELS:
            model.if_off_policy = True
        else:
            model.if_off_policy = False

        if model_kwargs is not None:
            try:
                model.learning_rate = model_kwargs["learning_rate"]
                model.batch_size = model_kwargs["batch_size"]
                model.gamma = model_kwargs["gamma"]
                model.net_dim = model_kwargs["net_dimension"]
                model.target_step = model_kwargs["target_step"]
                model.eval_gap = model_kwargs["eval_time_gap"]
            except BaseException:
                raise ValueError(
                    "Fail to read arguments, please check 'model_kwargs' input."
                )
        return model

    def train_model(self, model, cwd, total_timesteps=5000):
        model.cwd = cwd
        model.break_step = total_timesteps
        train_and_evaluate(model)

    @staticmethod
    def DRL_prediction(model_name, cwd, net_dimension, environment, gpu_id):
        if model_name not in MODELS:
            raise NotImplementedError("NotImplementedError")
        agent = MODELS[model_name]
        environment.env_num = 1

        args = Arguments(agent=agent, env=environment)

        args.cwd = cwd
        args.net_dim = net_dimension
        # load agent
        try:
            agent = init_agent(args, gpu_id=gpu_id)
            act = agent.act
            device = agent.device
        except BaseException:
            raise ValueError("Fail to load agent!")

        # test on the testing env
        _torch = torch
        state = environment.reset()
        episode_returns = list()  # the cumulative_return / initial_account
        episode_total_assets = list()
        episode_total_assets.append(environment.initial_total_asset)

        with _torch.no_grad():
            for i in range(environment.max_step):
                s_tensor = _torch.as_tensor((state,), device=device)
                a_tensor = act(s_tensor)  # action_tanh = act.forward()
                action = (
                    a_tensor.detach().cpu().numpy()[0]
                )  # not need detach(), because with torch.no_grad() outside
                state, reward, done, _ = environment.step(action)

                total_asset = (
                        environment.cash
                        + (
                                environment.price_array[environment.time] * environment.stocks
                        ).sum()
                )
                episode_total_assets.append(total_asset)
                episode_return = total_asset / environment.initial_total_asset
                episode_returns.append(episode_return)
                if done:
                    break
        Logger('DRL_prediction').info("Test Finished!")
        Logger('DRL_prediction').info(f"episode_return: {episode_return - 1}")
        return episode_total_assets
