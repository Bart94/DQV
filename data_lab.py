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

    def __str__(self):
        if self.act_tuple is not None:
            s = self._beautify_tuple(self.act_tuple) + " "
        else:
            s = ""
        return s + self._beautify_tuple(self.act_m_tuple)

    def _beautify_tuple(self, data):
        s = self._get_info(data)
        ac = s['ac'].hex()
        s = str((ac, s['h'], s['t']))
        return s
