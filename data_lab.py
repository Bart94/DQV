class DataLab:
    __slots__ = ['act_m_tuple', 'act_tuple']

    def __init__(self, at):
        self.act_m_tuple = at[0]
        self.act_tuple = None

        if len(at) > 1:
            self.act_tuple = at[1]

    def get_act_tuple(self):
        return self._get_info(self.act_tuple) if self.act_tuple is not None else None

    def get_act_m_tuple(self):
        return self._get_info(self.act_m_tuple)

    def _get_info(self, at):
        return {'ac': at[0], 'h': at[1], 't': at[2]}