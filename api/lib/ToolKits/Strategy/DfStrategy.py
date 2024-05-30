
def

def allInclude(df):
        return df.loc[df[FilterPather.field].apply(lambda x: all(str in x for str in FilterPather.constrainStr_List))]


def anyInclude(df):
        return df.loc[df[FilterPather.field].apply(lambda x: any(str in x for str in FilterPather.constrainStr_List))]


def allExclude(df):
        return df.loc[df[FilterPather.field].apply(lambda x: any(str in x for str in FilterPather.constrainStr_List))]