class DataLab:
    __slots__ = ['act_m_tuple', 'act_tuple']

    def __init__(self, at):
        self.act_m_tuple = at[0]
        self.act_tuple = None

        if len(at) > 1:
            self.act_tuple = at[1]

    def get_act_tuple(self):
        return self.act_tuple

    def get_act_m_tuple(self):
        return self.act_m_tuple

    def get_info(self, at):
        return {'ac': at[0], 'h': at[1], 't': at[2]}